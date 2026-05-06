# ParisBot - Expert Football RAG

Un chatbot expert en football propulsé par un RAG (Retrieval Augmented Generation) connecté à Wikipedia.
ParisBot est un ultra fan du PSG qui connait tout du football et n'hésite pas à tacler l'OM.

## Architecture

```
fetch_wikipedia.py  → télécharge les articles Wikipedia (~350 articles)
build_chunks.py     → découpe les articles en chunks (500 mots, overlap 100)
vector_db.py        → vectorise et stocke les chunks dans ChromaDB
rag.py              → connecte ChromaDB au LLM Groq
main.py             → interface terminal interactive
app.py              → interface Streamlit
config.py           → hyperparamètres centralisés
context.txt         → personnalité et instructions du LLM
```

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/OKO3210/football-rag.git
cd football-rag
git checkout main
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

### Étape 1 — Télécharger les articles Wikipedia
```bash
python fetch_wikipedia.py
```
Télécharge ~350 articles football dans `wikipedia_football.json`.
Idempotent : ne retélécharge pas les articles déjà présents, ajoute uniquement les nouveaux.

### Étape 2 — Construire les chunks
```bash
python build_chunks.py
```
Découpe les articles en chunks de 500 mots avec un overlap de 100 mots.
Résultat sauvegardé dans `chunks_football.json`.
Idempotent : si le fichier existe déjà, le chargement est direct.

### Étape 3 — Créer la base vectorielle
```bash
python vector_db.py
```
Vectorise les chunks avec `distiluse-base-multilingual-cased-v2` et les stocke dans ChromaDB.
Le dossier `football_knowledge/` n'est pas sur Git — à régénérer localement.

### Étape 4a — Lancer l'interface terminal
```bash
python main.py
```
Boucle interactive dans le terminal. Tape `exit` pour quitter.

### Étape 4b — Lancer l'interface Streamlit
```bash
streamlit run app.py
```
Interface web avec design PSG, bulles de chat et bouton Reset.

## Principes techniques

- **RAG** : le LLM répond uniquement depuis la base de connaissances Wikipedia — pas d'hallucination
- **Chunking** : 500 mots par chunk, overlap 100 mots pour ne pas couper le sens
- **Embedding** : modèle `distiluse-base-multilingual-cased-v2` (multilingue, léger)
- **Vector DB** : ChromaDB avec recherche par similarité cosinus
- **LLM** : Llama 3.3 70B via API Groq
- **Idempotence** : aucune étape ne refait ce qui est déjà fait

## Couverture des données

- **Joueurs** : ~100 joueurs actuels et légendes
- **Clubs** : ~60 clubs des 6 grands championnats européens
- **Saisons** : championnats et LDC de 2008 à 2025 (généré automatiquement)
- **Compétitions** : Coupes du monde 1998-2022, Euros 2000-2024, CAN, Copa América
- **Récompenses** : Ballons d'or 2018-2024

## Fichiers ignorés par Git
- `.env` (clé API)
- `env/` (environnement virtuel)
- `wikipedia_football.json` (données volumineuses)
- `chunks_football.json` (données volumineuses)
- `football_knowledge/` (base ChromaDB)
