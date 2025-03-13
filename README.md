# 🌐 Web Content Extraction API 📄

## 🔥 Votre passerelle vers l'extraction intelligente de contenu web 🔥

[![GitHub stars](https://img.shields.io/github/stars/simonpierreboucher0/web-content-api?style=social)](https://github.com/simonpierreboucher0/web-content-api/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.105.0+-green.svg)](https://fastapi.tiangolo.com/)

---

## ✨ Caractéristiques principales

📄 **Extraction puissante** - Récupérez le contenu brut et traité des pages web  
🧩 **Normalisation des données** - Format standardisé pour faciliter l'intégration  
⚡ **Haute performance** - Mise en cache intelligente des résultats  
🛡️ **Robustesse intégrée** - Gestion avancée des erreurs et des timeouts  
📊 **Logging détaillé** - Suivi complet des opérations d'extraction  
🌍 **Support multilingue** - Extraction du contenu en plusieurs langues  

---

## 🤖 Moteur d'extraction pris en charge

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
git clone https://github.com/simonpierreboucher0/WEB-EXTRACTION.git
cd WEB-EXTRACTION
```

### 2️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurer votre clé API
Créez un fichier `.env` avec votre clé:
```ini
TAVILY_KEY=votre_clé_tavily
```

---

## 🚀 Guide d'utilisation rapide

### ▶️ Démarrer le serveur
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 🌐 Documentation interactive
Accédez à l'interface Swagger pour tester l'API:
```
http://localhost:8001/docs
```

### 📄 Extraction simple avec Tavily
```bash
curl -X 'POST' \
  'http://localhost:8001/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "include_images": true,
    "extract_depth": "basic"
  }'
```

### 📚 Extraction de plusieurs URLs
```bash
curl -X 'POST' \
  'http://localhost:8001/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": [
      "https://en.wikipedia.org/wiki/Artificial_intelligence",
      "https://arxiv.org/abs/2307.06435"
    ],
    "include_images": true
  }'
```

---

## 📊 Structure complète des requêtes

```json
{
  "urls": "https://example.com/page",            // 🔗 URL ou liste d'URLs (obligatoire)
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
      "author": null,                                  // ✍️ Auteur (si disponible)
      "published_date": null,                          // 📅 Date de publication (si disponible)
      "images": [                                       // 🖼️ Images extraites
        {
          "url": "https://example.com/image.jpg",      // 🔗 URL de l'image
          "alt_text": "Description de l'image",        // 📝 Texte alternatif
          "width": 800,                                // 📐 Largeur en pixels
          "height": 600                                // 📐 Hauteur en pixels
        }
      ],
      "links": null                                    // 🔗 Liens extraits (si demandés)
    }
  ],
  "failed_urls": [],                                   // ❌ URLs qui ont échoué
  "engine": "tavily",                                  // 🌐 Moteur utilisé
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

### 📑 Extraction parallèle de plusieurs URLs

```python
import requests
import concurrent.futures

def batch_extract(urls):
    # Découper en lots de 5 URLs
    batches = [urls[i:i+5] for i in range(0, len(urls), 5)]
    all_results = []
    failed_urls = []
    
    def extract_batch(batch):
        try:
            response = requests.post(
                "http://localhost:8001/extract",
                json={
                    "urls": batch,
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

results, failures = batch_extract(news_sites)
print(f"Extractions réussies: {len(results)}, Échecs: {len(failures)}")
```

### 📰 Extraction d'articles d'actualité

```python
import requests
import json
from datetime import datetime

def extract_news_article(url):
    response = requests.post(
        "http://localhost:8001/extract",
        json={
            "urls": url,
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

L'API intègre un endpoint de santé complet pour surveiller l'état du service:

```bash
curl -X GET http://localhost:8001/health
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
  'http://localhost:8001/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "include_images": true
  }'
  
# Requête identique (depuis le cache, beaucoup plus rapide)
curl -X 'POST' \
  'http://localhost:8001/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "include_images": true
  }'
```

### 📄 Extraction avec différentes profondeurs
Adaptez la profondeur d'extraction selon vos besoins:

```bash
# Extraction basique (plus rapide)
curl -X 'POST' \
  'http://localhost:8001/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://example.com/article",
    "extract_depth": "basic"
  }'

# Extraction avancée (plus complète)
curl -X 'POST' \
  'http://localhost:8001/extract' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": "https://example.com/article",
    "extract_depth": "advanced"
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

### 🚀 Comment optimiser les performances?
Activez la mise en cache, limitez l'extraction aux données nécessaires (désactivez les images si non requises), et utilisez la profondeur d'extraction appropriée.

### 🌐 L'API fonctionne-t-elle sur tous les sites web?
La plupart des sites modernes sont supportés, mais certains peuvent avoir des protections anti-scraping ou des structures complexes qui rendent l'extraction difficile.

### ⚙️ Comment adapter l'API à mes besoins spécifiques?
Le code source est conçu pour être facilement extensible - vous pouvez ajouter de nouveaux moteurs d'extraction ou personnaliser les paramètres existants.

### 📱 Puis-je intégrer cette API dans des applications mobiles?
Oui, l'API peut être appelée depuis n'importe quelle application capable d'effectuer des requêtes HTTP, y compris les applications mobiles.

### 🔍 Quelles sont les limites d'extraction?
Les limites dépendent principalement du plan de l'API Tavily que vous utilisez. Consultez leur documentation pour plus de détails sur les quotas et les limites.

---

## 👨‍💻 Auteurs

- 🚀 [Simon-Pierre Boucher](https://github.com/simonpierreboucher0) - Créateur principal

---

<p align="center">
⭐ N'oubliez pas de mettre une étoile si ce projet vous a été utile! ⭐
</p>

<p align="center">
🔗 <a href="https://github.com/simonpierreboucher0/WEB-EXTRACTION">GitHub</a> | 
🐛 <a href="https://github.com/simonpierreboucher0/WEB-EXTRACTION/issues">Signaler un problème</a> | 
💡 <a href="https://github.com/simonpierreboucher0/WEB-EXTRACTION/discussions">Discussions</a>
</p>
