# 🌐 Web Content Extraction API 📄

## 🔥 Votre passerelle unifiée vers l'extraction intelligente de contenu web 🔥

[![GitHub stars](https://img.shields.io/github/stars/simonpierreboucher0/web-content-api?style=social)](https://github.com/simonpierreboucher0/web-content-api/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.105.0+-green.svg)](https://fastapi.tiangolo.com/)

---

## ✨ Caractéristiques principales

📄 **Extraction puissante** - Récupérez le contenu brut et traité des pages web  
🔄 **Interface unifiée** - Une seule API pour différents moteurs d'extraction  
🧩 **Normalisation des données** - Format standardisé quelle que soit la source  
⚡ **Haute performance** - Mise en cache intelligente des résultats  
🛡️ **Robustesse intégrée** - Gestion avancée des erreurs et des timeouts  
📊 **Logging détaillé** - Suivi complet des opérations d'extraction  
🌍 **Support multilingue** - Extraction du contenu en plusieurs langues  
🔌 **Failover automatique** - Bascule intelligente entre les fournisseurs  

---

## 🤖 Moteurs d'extraction pris en charge

### 🟣 Exa AI
Extraction sophistiquée avec analyse sémantique avancée.

| Fonctionnalité | Description | Avantage |
|----------------|-------------|----------|
| 📄 **Extraction de texte** | Récupération du contenu principal | Élimination du bruit et publicités |
| 🖼️ **Récupération d'images** | Extraction des images pertinentes | Contenu visuel associé |
| 🔗 **Analyse des liens** | Collecte des liens internes et externes | Cartographie complète du contenu |
| 📋 **Métadonnées structurées** | Extraction de title, author, date... | Information contextuelle enrichie |
| 📑 **Sous-pages intelligentes** | Exploration des pages liées pertinentes | Contenu connexe automatiquement détecté |
| 📊 **Scores de pertinence** | Évaluation de sections importantes | Identification des passages clés |
| 🔍 **Mise en évidence** | Extraction des passages significatifs | Points essentiels rapidement identifiés |
| 📝 **Génération de résumés** | Synthèse automatique du contenu | Vue d'ensemble instantanée |

### 🟢 Tavily
Extraction précise optimisée pour la récupération d'information structurée.

| Fonctionnalité | Description | Avantage |
|----------------|-------------|----------|
| 🔎 **Profondeur d'extraction** | Modes basic et advanced | Flexibilité selon les besoins |
| 📜 **Contenu brut** | Texte original de la page | Données non filtrées pour analyse personnalisée |
| 📊 **Contenu structuré** | Texte nettoyé et organisé | Facilite le traitement ultérieur |
| 🏗️ **Extraction de structure** | Organisation hiérarchique du contenu | Compréhension de l'architecture de la page |
| 🖼️ **Images contextuelles** | Capture des images avec métadonnées | Enrichissement visuel du contenu |
| 🔍 **Détection de contenu dynamique** | Gestion du JavaScript et contenu chargé dynamiquement | Extraction complète même sur sites modernes |
| ⏱️ **Optimisation des performances** | Extraction rapide et efficace | Traitement de grand volume d'URLs |
| 🧩 **Compatibilité multiformat** | Support de divers formats web | Large couverture de sites |

---

## 🛠️ Installation facile en 3 étapes

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/simonpierreboucher0/web-content-api.git
cd web-content-api
```

### 2️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurer vos clés API
Créez un fichier `.env` avec vos clés:
```ini
TAVILY_KEY=votre_clé_tavily
EXA_KEY=votre_clé_exa
```

> 💡 **Astuce**: Vous n'avez besoin de fournir que les clés pour les moteurs que vous allez utiliser!

---

## 🚀 Guide d'utilisation rapide

### ▶️ Démarrer le serveur
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Documentation interactive
Accédez à l'interface Swagger pour tester l'API:
```
http://localhost:8000/docs
```

### 📄 Extraction simple avec Tavily
```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "engine": "tavily",
    "include_images": true,
    "extract_depth": "basic"
  }'
```

### 📑 Extraction avancée avec Exa
```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "engine": "exa",
    "include_images": true,
    "include_links": true
  }'
```

### 🔄 Extraction automatique (meilleur moteur disponible)
```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "engine": "auto",
    "include_images": true
  }'
```

### 📚 Extraction de plusieurs URLs
```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": [
      "https://en.wikipedia.org/wiki/Artificial_intelligence",
      "https://arxiv.org/abs/2307.06435"
    ],
    "engine": "exa",
    "include_links": true
  }'
```

---

## 📊 Structure complète des requêtes

```json
{
  "urls": "https://example.com/page",            // 🔗 URL ou liste d'URLs (obligatoire)
  "engine": "exa",                               // 🌐 Moteur d'extraction (exa, tavily, auto)
  "include_images": true,                        // 🖼️ Inclure les images
  "include_raw_content": false,                  // 📜 Inclure le contenu brut non traité
  "extract_depth": "advanced",                   // 🔍 Profondeur d'extraction (basic, advanced)
  "include_links": true,                         // 🔗 Inclure les liens trouvés
  "max_tokens": 10000                            // 📏 Limite de taille du texte extrait
}
```

---

## 📋 Format des résultats

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000", // 🆔 Identifiant unique de requête
  "urls": ["https://example.com/page"],                // 🔗 URLs d'origine
  "results": [                                         // 📊 Liste des résultats
    {
      "url": "https://example.com/page",               // 🔗 URL de la page
      "title": "Titre de la page web",                 // 📝 Titre de la page
      "content": "Contenu principal extrait...",       // 📄 Contenu traité
      "raw_content": "HTML brut ou texte complet...",  // 📜 Contenu brut (si demandé)
      "author": "Nom de l'auteur",                     // ✍️ Auteur si disponible
      "published_date": "2024-01-15T14:30:00Z",        // 📅 Date de publication
      "images": [                                       // 🖼️ Images extraites
        {
          "url": "https://example.com/image.jpg",      // 🔗 URL de l'image
          "alt_text": "Description de l'image",        // 📝 Texte alternatif
          "width": 800,                                // 📐 Largeur en pixels
          "height": 600                                // 📐 Hauteur en pixels
        }
      ],
      "links": [                                       // 🔗 Liens extraits
        {
          "url": "https://example.com/related",        // 🔗 URL du lien
          "text": "Texte du lien",                     // 📝 Texte d'ancrage
          "is_internal": true                          // 🏠 Lien interne ou externe
        }
      ],
      "favicon": "https://example.com/favicon.ico",    // 🔖 Favicon du site
      "subpages": [                                    // 📑 Sous-pages liées
        {
          "url": "https://example.com/subpage",        // 🔗 URL de la sous-page
          "title": "Titre de la sous-page",            // 📝 Titre
          "content": "Extrait de la sous-page..."      // 📄 Contenu
        }
      ]
    }
  ],
  "failed_urls": [],                                   // ❌ URLs qui ont échoué
  "engine": "exa",                                     // 🌐 Moteur utilisé
  "time_taken": 0.35,                                  // ⏱️ Temps d'exécution (secondes)
  "cached": false,                                     // 🔄 Résultat depuis le cache?
  "status": "ok",                                      // ✅ État de la requête
  "cost_info": {                                       // 💰 Informations de coût
    "total_urls": 1,                                   // 🔢 Nombre total d'URLs
    "successful_extractions": 1,                       // ✅ Extractions réussies
    "cached_results": 0,                               // 🔄 Résultats depuis le cache
    "api_calls": 1                                     // 📞 Nombre d'appels API effectués
  }
}
```

---

## 💡 Cas d'utilisation avancés

### 🔄 Failover automatique entre moteurs
Si un moteur est indisponible, l'API bascule automatiquement vers le suivant:

```python
import requests

def extract_with_failover(url, engines=["exa", "tavily"]):
    for engine in engines:
        try:
            response = requests.post(
                "http://localhost:8000/extract",
                json={
                    "urls": url,
                    "engine": engine,
                    "include_images": True
                },
                timeout=20
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Échec avec {engine}: {str(e)}")
    return {"error": "Tous les moteurs ont échoué"}

results = extract_with_failover("https://arxiv.org/abs/2307.06435")
```

### 📑 Extraction parallèle de plusieurs URLs

```python
import requests
import concurrent.futures

def batch_extract(urls, engine="auto"):
    # Découper en lots de 5 URLs
    batches = [urls[i:i+5] for i in range(0, len(urls), 5)]
    all_results = []
    failed_urls = []
    
    def extract_batch(batch):
        try:
            response = requests.post(
                "http://localhost:8000/extract",
                json={
                    "urls": batch,
                    "engine": engine,
                    "include_images": True,
                    "extract_depth": "basic"
                },
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return data["results"], data["failed_urls"]
            return [], batch
        except Exception as e:
            print(f"Erreur batch: {str(e)}")
            return [], batch
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(extract_batch, batch) for batch in batches]
        
        for future in concurrent.futures.as_completed(futures):
            results, failures = future.result()
            all_results.extend(results)
            failed_urls.extend(failures)
    
    return all_results, failed_urls

# Liste d'URLs à traiter
news_sites = [
    "https://www.reuters.com/technology/ai",
    "https://www.theverge.com/ai-artificial-intelligence",
    "https://www.wired.com/category/artificial-intelligence/",
    "https://venturebeat.com/category/ai/",
    "https://techcrunch.com/category/artificial-intelligence/",
    "https://www.technologyreview.com/topic/artificial-intelligence/",
    "https://www.zdnet.com/topic/artificial-intelligence/"
]

results, failures = batch_extract(news_sites, "exa")
print(f"Extractions réussies: {len(results)}, Échecs: {len(failures)}")
```

### 📊 Comparaison d'extraction entre moteurs

```python
import requests
import concurrent.futures

def compare_extraction_engines(url):
    engines = ["exa", "tavily"]
    results = {}
    
    def extract_with_engine(engine):
        try:
            response = requests.post(
                "http://localhost:8000/extract",
                json={
                    "urls": url, 
                    "engine": engine,
                    "include_images": True,
                    "extract_depth": "advanced" if engine == "tavily" else "basic"
                },
                timeout=25
            )
            if response.status_code == 200:
                return engine, response.json()
            return engine, {"error": f"Status code: {response.status_code}"}
        except Exception as e:
            return engine, {"error": str(e)}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for engine, result in executor.map(extract_with_engine, engines):
            results[engine] = result
    
    return results

comparison = compare_extraction_engines("https://en.wikipedia.org/wiki/Machine_learning")

# Analyse des résultats
for engine, data in comparison.items():
    if "error" in data:
        print(f"⚠️ {engine}: Erreur - {data['error']}")
        continue
        
    print(f"🔍 {engine}: Extraction en {data['time_taken']:.2f}s")
    
    if data["results"]:
        content_length = len(data["results"][0].get("content", ""))
        image_count = len(data["results"][0].get("images", []))
        print(f"  📄 Taille du contenu: {content_length} caractères")
        print(f"  🖼️ Nombre d'images: {image_count}")
        
        if "links" in data["results"][0]:
            link_count = len(data["results"][0]["links"])
            print(f"  🔗 Nombre de liens: {link_count}")
```

### 📰 Extraction d'articles d'actualité

```python
import requests
import json
from datetime import datetime

def extract_news_article(url):
    response = requests.post(
        "http://localhost:8000/extract",
        json={
            "urls": url,
            "engine": "exa",  # Exa est souvent meilleur pour les articles
            "include_images": True
        }
    )
    
    if response.status_code != 200:
        return {"error": f"Extraction failed: {response.status_code}"}
    
    data = response.json()
    
    if not data["results"]:
        return {"error": "No content extracted"}
    
    article = data["results"][0]
    
    # Formater l'article
    formatted_article = {
        "title": article.get("title", "Untitled Article"),
        "url": article.get("url"),
        "author": article.get("author", "Unknown Author"),
        "published_date": article.get("published_date"),
        "content": article.get("content", "").strip(),
        "word_count": len(article.get("content", "").split()),
        "reading_time_minutes": round(len(article.get("content", "").split()) / 200),  # ~200 mots/minute
        "main_image": article.get("images", [{}])[0].get("url") if article.get("images") else None,
        "extraction_date": datetime.now().isoformat()
    }
    
    return formatted_article

# Exemple
news_url = "https://www.theverge.com/2024/1/15/24039104/openai-anthropic-meta-google-ai-regulation"
article = extract_news_article(news_url)
print(json.dumps(article, indent=2))
```

---

## 🧪 Tests de santé et surveillance

L'API intègre un endpoint de santé complet pour surveiller l'état des services:

```bash
curl -X GET http://localhost:8000/health
```

Exemple de réponse:
```json
{
  "status": "healthy",
  "time": "2024-08-07T14:35:22.451Z",
  "version": "1.0.0",
  "uptime": "2 days, 5:12:30",
  "memory_usage": "98452 KB",
  "hostname": "extraction-api-server",
  "cache_entries": 145,
  "api_statuses": {
    "exa": "ok",
    "tavily": "ok"
  },
  "response_time": "0.0823s"
}
```

---

## 🔒 Sécurité et bonnes pratiques

- 🔑 **Gestion des clés**: Stockées localement dans `.env`, jamais exposées
- 🛡️ **Rate Limiting**: Protection contre les abus via limitation de taux
- 🔒 **CORS configurable**: Protection contre les requêtes non autorisées
- 📝 **Logging sécurisé**: Masquage automatique des informations sensibles
- ⏱️ **Timeouts contrôlés**: Évite les requêtes bloquantes
- 🔄 **Retry avec backoff**: Gestion intelligente des erreurs temporaires
- 🧹 **Nettoyage des caches**: Libération automatique des ressources

---

## 📚 Fonctionnalités avancées

### 📋 Système de mise en cache
Le système met intelligemment en cache les résultats pour optimiser les performances:

```bash
# Première requête (non mise en cache)
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "engine": "tavily",
    "include_images": true
  }'
  
# Requête identique (depuis le cache, beaucoup plus rapide)
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "engine": "tavily",
    "include_images": true
  }'
```

### 📄 Extraction avec différentes profondeurs
Adaptez la profondeur d'extraction selon vos besoins:

```bash
# Extraction basique (plus rapide)
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://example.com/article",
    "engine": "tavily",
    "extract_depth": "basic"
  }'

# Extraction avancée (plus complète)
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://example.com/article",
    "engine": "tavily",
    "extract_depth": "advanced"
  }'
```

### 🔗 Extraction de contenu avec liens et sous-pages
Obtenez une analyse plus complète d'une page et de ses liens:

```bash
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://docs.python.org/3/tutorial/",
    "engine": "exa",
    "include_links": true,
    "include_images": true
  }'
```

---

## 🤝 Contribution

Les contributions sont les bienvenues! Voici comment participer:

1. 🍴 **Fork** le dépôt
2. 🔄 Créez une **branche** (`git checkout -b feature/ma-fonctionnalite`)
3. ✏️ Faites vos **modifications**
4. 📦 **Commit** vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
5. 📤 **Push** vers la branche (`git push origin feature/ma-fonctionnalite`)
6. 🔍 Ouvrez une **Pull Request**

### 💼 Idées de contributions

- 🔌 Support de nouveaux moteurs d'extraction
- 🧰 Options d'extraction additionnelles
- 📊 Visualisation du contenu extrait
- 🌐 Interface utilisateur web simple
- 📝 Expansion de la documentation
- 🧪 Tests additionnels

---

## 📜 Licence

Ce projet est sous licence [MIT](LICENSE) - voir le fichier LICENSE pour plus de détails.

---

## ❓ FAQ

### 🔄 Quelle est la différence entre les moteurs d'extraction?
- **Exa AI**: Meilleur pour l'extraction structurée et les métadonnées, avec support des sous-pages
- **Tavily**: Performances supérieures pour la récupération de contenu brut et l'extraction profonde

### 💰 Quel moteur est le plus économique?
Les coûts varient selon l'utilisation, mais les deux services offrent des plans gratuits généreux pour commencer.

### 🚀 Comment optimiser les performances?
Activez la mise en cache, limitez l'extraction aux données nécessaires (désactivez les images si non requises), et utilisez la profondeur d'extraction appropriée.

### 🌐 L'API fonctionne-t-elle sur tous les sites web?
La plupart des sites modernes sont supportés, mais certains peuvent avoir des protections anti-scraping ou des structures complexes qui rendent l'extraction difficile.

### ⚙️ Comment adapter l'API à mes besoins spécifiques?
Le code source est conçu pour être facilement extensible - vous pouvez ajouter de nouveaux moteurs d'extraction ou personnaliser les paramètres existants.

---

## 👨‍💻 Auteurs

- 🚀 [Simon-Pierre Boucher](https://github.com/simonpierreboucher0) - Créateur principal

---

<p align="center">
⭐ N'oubliez pas de mettre une étoile si ce projet vous a été utile! ⭐
</p>

<p align="center">
🔗 <a href="https://github.com/simonpierreboucher0/web-content-api">GitHub</a> | 
🐛 <a href="https://github.com/simonpierreboucher0/web-content-api/issues">Signaler un problème</a> | 
💡 <a href="https://github.com/simonpierreboucher0/web-content-api/discussions">Discussions</a>
</p>
