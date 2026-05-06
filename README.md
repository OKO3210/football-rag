# ParisBot - Expert Football RAG

Un chatbot expert en football propulsé par un RAG (Retrieval Augmented Generation) connecté à Wikipedia.
ParisBot est un ultra fan du PSG qui connait tout du football et n'hésite pas à tacler l'OM.

## Architecture

```
fetch_wikipedia.py  → télécharge les articles Wikipedia (JSON)
build_chunks.py     → découpe les articles en chunks (500 mots, overlap 100)
vector_db.py        → vectorise et stocke les chunks dans ChromaDB
rag.py              → connecte ChromaDB au LLM Groq
app.py              → interface Streamlit
config.py           → hyperparamètres centralisés
context.txt         → personnalité et instructions du LLM
```

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/OKO3210/football-rag.git
cd football-rag
git checkout my_first_rag
```

### 2. Créer et activer l'environnement virtuel
```bash
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Mac/Linux
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Créer le fichier .env
Créer un fichier `.env` à la racine avec votre clé API Groq :
```
GROQ_API_KEY=votre_clé_ici
```
Obtenez une clé gratuite sur : https://console.groq.com

## Lancement (ordre obligatoire)

### Étape 1 - Télécharger les articles Wikipedia
```bash
python fetch_wikipedia.py
```
Télécharge ~150 articles football dans `wikipedia_football.json`.
Idempotent : ne retélécharge pas les articles déjà présents.

### Étape 2 - Construire les chunks
```bash
python build_chunks.py
```
Découpe les articles en chunks de 500 mots avec un overlap de 100 mots.
Résultat sauvegardé dans `chunks_football.json`.

### Étape 3 - Créer la base vectorielle
```bash
python vector_db.py
```
Vectorise les chunks et les stocke dans ChromaDB (dossier `football_knowledge`).
Ce dossier n'est pas sur Git (trop lourd) - à régénérer localement.

### Étape 4 - Lancer l'application
```bash
streamlit run app.py
```

## Tester le RAG sans l'interface
```bash
python rag.py
```

## Principes techniques

- **RAG** : Retrieval Augmented Generation - le LLM répond uniquement depuis la base de connaissances
- **Chunking** : 500 mots par chunk, overlap de 100 mots pour ne pas couper le sens
- **Embedding** : modèle `distiluse-base-multilingual-cased-v2` (multilingue)
- **Vector DB** : ChromaDB avec recherche par similarité cosinus
- **LLM** : Llama 3.3 70B via API Groq
- **Idempotence** : aucune étape ne refait ce qui est déjà fait

## Fichiers ignorés par Git
- `.env` (clé API)
- `env/` (environnement virtuel)
- `wikipedia_football.json` (données volumineuses)
- `chunks_football.json` (données volumineuses)
- `football_knowledge/` (base ChromaDB)
