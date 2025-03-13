from fastapi import FastAPI, HTTPException, Query, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from enum import Enum
from pydantic import BaseModel, Field, validator
import httpx
import os
from typing import List, Optional, Dict, Any, Union
from dotenv import load_dotenv
import time
import logging
import json
from datetime import datetime, timedelta
import asyncio
from functools import lru_cache
import uuid
import socket
import traceback
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("extraction_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("extraction_api")

# Charger les variables d'environnement
load_dotenv()

# API Keys
TAVILY_KEY = os.getenv("TAVILY_KEY")

# Configuration timeout et retry
TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))
MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "2"))
CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", "60"))

# Limiteur de taux de requêtes
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="API d'Extraction de Contenu Web",
    description="Cette API permet d'extraire le contenu des pages web en utilisant le service Tavily.",
    version="1.0.0",
)

# Middleware pour la gestion des erreurs de limite de taux
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware pour la compression des réponses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExtractionEngine(str, Enum):
    tavily = "tavily"

class ApiStatus(str, Enum):
    ok = "ok"
    degraded = "degraded"
    unavailable = "unavailable"

class ExtractDepth(str, Enum):
    basic = "basic"
    advanced = "advanced"

class UrlExtractionResult(BaseModel):
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    raw_content: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[str] = None
    images: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    links: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    favicon: Optional[str] = None
    subpages: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class Error(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ExtractionResponse(BaseModel):
    request_id: str
    urls: List[str]
    results: List[UrlExtractionResult]
    failed_urls: List[str] = Field(default_factory=list)
    engine: ExtractionEngine
    time_taken: float
    cached: bool = False
    status: ApiStatus = ApiStatus.ok
    error: Optional[Error] = None
    cost_info: Optional[Dict[str, Any]] = None

class ExtractionRequest(BaseModel):
    urls: Union[str, List[str]] = Field(..., description="URL ou liste d'URLs à extraire")
    include_images: bool = Field(default=False, description="Inclure les images dans les résultats")
    include_raw_content: bool = Field(default=False, description="Inclure le contenu brut non traité")
    extract_depth: ExtractDepth = Field(default=ExtractDepth.basic, description="Profondeur d'extraction")
    include_links: bool = Field(default=False, description="Inclure les liens trouvés dans la page")
    max_tokens: Optional[int] = Field(default=None, description="Limite du nombre de tokens extraits")
    
    @validator('urls')
    def validate_urls(cls, v):
        if isinstance(v, str):
            v = [v]
        
        if not v or len(v) == 0:
            raise ValueError("Au moins une URL doit être fournie")
            
        for url in v:
            if not url.startswith(('http://', 'https://')):
                raise ValueError(f"L'URL '{url}' doit commencer par http:// ou https://")
        
        return v

# Cache en mémoire pour les résultats d'extraction
# Clé de cache: "{engine}:{url}:{include_images}:{include_raw_content}:{extract_depth}"
extraction_cache = {}

def generate_cache_key(engine: str, url: str, include_images: bool, include_raw_content: bool, extract_depth: str) -> str:
    """Génère une clé unique pour le cache en fonction des paramètres d'extraction"""
    return f"{engine}:{url}:{include_images}:{include_raw_content}:{extract_depth}"

def get_cached_result(cache_key: str) -> Optional[Dict[str, Any]]:
    """Récupère un résultat du cache s'il est valide et non expiré"""
    if cache_key in extraction_cache:
        entry = extraction_cache[cache_key]
        if datetime.now() < entry["expires_at"]:
            logger.info(f"Cache hit for key: {cache_key}")
            return entry["data"]
        else:
            # Nettoyer les entrées expirées
            logger.info(f"Cache expired for key: {cache_key}")
            del extraction_cache[cache_key]
    return None

def cache_result(cache_key: str, result: Dict[str, Any]) -> None:
    """Met en cache un résultat d'extraction"""
    extraction_cache[cache_key] = {
        "data": result,
        "expires_at": datetime.now() + timedelta(minutes=CACHE_TTL_MINUTES)
    }
    logger.info(f"Cached result for key: {cache_key}")
    
    # Nettoyer le cache si trop gros (simple LRU)
    if len(extraction_cache) > 1000:
        oldest = min(extraction_cache.items(), key=lambda x: x[1]["expires_at"])
        del extraction_cache[oldest[0]]

async def check_api_health(engine: ExtractionEngine) -> ApiStatus:
    """Vérifie la santé de l'API externe"""
    try:
        if engine == ExtractionEngine.tavily:
            if not TAVILY_KEY:
                return ApiStatus.unavailable
            url = "https://api.tavily.com/health"  # Endpoint fictif, ajustez selon l'API réelle
            headers = {"Authorization": f"Bearer {TAVILY_KEY}"}
            
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                return ApiStatus.ok
            else:
                logger.warning(f"API health check for {engine} returned status {response.status_code}")
                return ApiStatus.degraded
                
    except Exception as e:
        logger.error(f"API health check for {engine} failed: {str(e)}")
        return ApiStatus.unavailable

async def extract_with_tavily(urls: List[str], include_images: bool = False, extract_depth: str = "basic") -> Dict[str, Any]:
    """Extraction de contenu avec Tavily avec gestion des erreurs et retries"""
    url = "https://api.tavily.com/extract"
    headers = {
        "Authorization": f"Bearer {TAVILY_KEY}",
        "Content-Type": "application/json"
    }
    
    # Préparer la payload avec un seul URL ou multiple selon le cas
    payload = {
        "urls": urls if len(urls) > 1 else urls[0],
        "include_images": include_images,
        "extract_depth": extract_depth
    }
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    return response.json()
                
                elif response.status_code == 429:  # Rate limit
                    if attempt < MAX_RETRIES:
                        wait_time = min(2 ** attempt, 10)  # Exponential backoff
                        logger.warning(f"Rate limit hit with Tavily API. Retrying in {wait_time}s. Attempt {attempt+1}/{MAX_RETRIES+1}")
                        await asyncio.sleep(wait_time)
                        continue
                
                # Autres erreurs
                error_detail = f"Erreur de l'API Tavily: {response.status_code}"
                try:
                    error_detail += f" - {response.json().get('error', '')}"
                except:
                    error_detail += f" - {response.text[:100]}"
                    
                logger.error(error_detail)
                raise HTTPException(status_code=response.status_code, detail=error_detail)
                
        except httpx.TimeoutException:
            if attempt < MAX_RETRIES:
                logger.warning(f"Timeout with Tavily API. Retrying. Attempt {attempt+1}/{MAX_RETRIES+1}")
                continue
            raise HTTPException(status_code=504, detail="Timeout lors de la requête à l'API Tavily")
            
        except httpx.RequestError as e:
            if attempt < MAX_RETRIES:
                logger.warning(f"Request error with Tavily API: {str(e)}. Retrying. Attempt {attempt+1}/{MAX_RETRIES+1}")
                continue
            raise HTTPException(status_code=502, detail=f"Erreur de requête à l'API Tavily: {str(e)}")
            
        except Exception as e:
            logger.error(f"Unexpected error with Tavily API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur inattendue lors de la requête à l'API Tavily: {str(e)}")
    
    # Si on arrive ici, c'est qu'on a épuisé les tentatives
    raise HTTPException(status_code=429, detail="Trop de tentatives échouées avec l'API Tavily")

def process_tavily_results(data: Dict[str, Any]) -> List[UrlExtractionResult]:
    """Traite les résultats bruts de Tavily en format standardisé"""
    results = []
    
    for item in data.get("results", []):
        result = UrlExtractionResult(
            url=item.get("url", ""),
            title=item.get("title", ""),
            content=item.get("raw_content", "")[:5000] if item.get("raw_content") else None,  # Limiter pour éviter des réponses trop grandes
            raw_content=item.get("raw_content"),
            images=item.get("images", [])
        )
        results.append(result)
    
    return results

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware pour logger les requêtes et leur temps d'exécution"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    
    # Capturer le corps de la requête pour le logging
    body = await request.body()
    if body:
        try:
            body_str = body.decode()
            # Ne pas loguer les infos sensibles comme les API keys
            if '"api_key"' in body_str or '"Authorization"' in body_str:
                body_str = "[CONTENU SENSIBLE MASQUÉ]"
        except:
            body_str = "[CORPS NON DÉCODABLE]"
    else:
        body_str = ""
    
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"[{request_id}] Request received - Method: {request.method}, Path: {request.url.path}, "
               f"Client: {client_host}, Query Params: {request.query_params}, Body: {body_str[:500]}")
    
    try:
        # Exécuter la requête
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        
        logger.info(f"[{request_id}] Request completed - Status: {response.status_code}, Time: {process_time:.4f}s")
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"[{request_id}] Exception during request: {str(e)}\n{traceback.format_exc()}")
        
        # Créer une réponse d'erreur cohérente
        error_detail = str(e)
        if isinstance(e, HTTPException):
            status_code = e.status_code
            error_detail = e.detail
        else:
            status_code = 500
        
        error_response = JSONResponse(
            status_code=status_code,
            content={
                "request_id": request_id,
                "error": {
                    "code": f"ERROR_{status_code}",
                    "message": "Une erreur est survenue lors du traitement de votre requête",
                    "details": {
                        "error": error_detail
                    }
                },
                "status": "error",
                "time_taken": process_time
            }
        )
        
        error_response.headers["X-Process-Time"] = str(process_time)
        error_response.headers["X-Request-ID"] = request_id
        
        return error_response

@app.post("/extract", response_model=ExtractionResponse)
@limiter.limit("15/minute")
async def extract_content(request: Request, extraction_request: ExtractionRequest):
    """
    Extrait le contenu des pages web à partir des URLs spécifiées.
    
    - **urls**: URL ou liste d'URLs à extraire
    - **include_images**: Inclure les images dans les résultats
    - **include_raw_content**: Inclure le contenu brut non traité
    - **extract_depth**: Profondeur d'extraction (basic, advanced)
    - **include_links**: Inclure les liens trouvés dans la page
    """
    request_id = request.state.request_id
    start_time = time.time()
    engine = ExtractionEngine.tavily
    urls = extraction_request.urls
    include_images = extraction_request.include_images
    include_raw_content = extraction_request.include_raw_content
    extract_depth = extraction_request.extract_depth
    include_links = extraction_request.include_links
    
    # Vérifier la disponibilité de l'API
    api_status = await check_api_health(engine)
    if api_status == ApiStatus.unavailable:
        return ExtractionResponse(
            request_id=request_id,
            urls=urls,
            results=[],
            failed_urls=urls,
            engine=engine,
            time_taken=time.time() - start_time,
            status=ApiStatus.unavailable,
            error=Error(
                code="API_UNAVAILABLE",
                message="Le service d'extraction Tavily n'est actuellement pas disponible",
                details={"info": "Veuillez réessayer plus tard"}
            )
        )
    
    # Pour l'instant, gérer les URLs une par une pour le cache
    all_results = []
    failed_urls = []
    cached_count = 0
    
    for url in urls:
        # Vérifier si le résultat est en cache
        cache_key = generate_cache_key(engine.value, url, include_images, include_raw_content, extract_depth.value)
        cached_result = get_cached_result(cache_key)
        
        if cached_result:
            all_results.extend(cached_result["results"])
            cached_count += 1
            continue
        
        try:
            # Extraire le contenu de l'URL avec Tavily
            data = await extract_with_tavily([url], include_images, extract_depth.value)
            url_results = process_tavily_results(data)
            
            # Mettre en cache
            cache_result(cache_key, {"results": url_results})
            
            all_results.extend(url_results)
                
        except Exception as e:
            logger.error(f"[{request_id}] Error extracting URL {url}: {str(e)}")
            failed_urls.append(url)
    
    # Préparer la réponse
    api_status = ApiStatus.ok if len(failed_urls) == 0 else ApiStatus.degraded
    if len(failed_urls) == len(urls):
        api_status = ApiStatus.unavailable
    
    response_data = {
        "request_id": request_id,
        "urls": urls,
        "results": all_results,
        "failed_urls": failed_urls,
        "engine": engine,
        "time_taken": time.time() - start_time,
        "cached": cached_count > 0,
        "status": api_status,
        "cost_info": {
            "total_urls": len(urls),
            "successful_extractions": len(urls) - len(failed_urls),
            "cached_results": cached_count,
            "api_calls": len(urls) - cached_count
        }
    }
    
    return ExtractionResponse(**response_data)

@app.get("/health")
async def health_check():
    """
    Endpoint de vérification de santé de l'API et des services externes
    """
    start_time = time.time()
    
    # Vérifier l'état de l'API Tavily
    try:
        tavily_status = await check_api_health(ExtractionEngine.tavily)
        
        # Vérifier le service lui-même
        memory_usage = f"{os.popen('ps -p %d -o rss | tail -1' % os.getpid()).read().strip()} KB"
        hostname = socket.gethostname()
        cache_size = len(extraction_cache)
        
        return {
            "status": "healthy",
            "time": datetime.now().isoformat(),
            "version": app.version,
            "uptime": os.popen("uptime").read().strip(),
            "memory_usage": memory_usage,
            "hostname": hostname,
            "cache_entries": cache_size,
            "api_statuses": {
                "tavily": tavily_status
            },
            "response_time": f"{time.time() - start_time:.4f}s"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "time": datetime.now().isoformat(),
            "error": str(e),
            "response_time": f"{time.time() - start_time:.4f}s"
        }

@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API d'Extraction de Contenu Web. Utilisez /extract pour extraire le contenu des pages web.",
        "docs": "/docs",
        "health": "/health",
        "version": app.version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
