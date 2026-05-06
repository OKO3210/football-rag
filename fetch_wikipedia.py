import wikipediaapi
import json
import os
from tqdm import tqdm

wiki = wikipediaapi.Wikipedia(
    language='fr',
    user_agent='football-rag/1.0'
)

ARTICLES = [
    # ── Joueurs actuels ──
    "Kylian Mbappé",
    "Vinicius Junior",
    "Jude Bellingham",
    "Erling Haaland",
    "Mohamed Salah",
    "Lamine Yamal",
    "Ousmane Dembélé",
    "Antoine Griezmann",
    "Lionel Messi",
    "Cristiano Ronaldo",
    "Neymar",
    "Pedri",
    "Gavi (footballeur)",
    "Rodri",
    "Toni Kroos",
    "Vinícius Júnior",
    "Bukayo Saka",
    "Phil Foden",
    "Marcus Rashford",
    "Rúben Dias",
    "Virgil van Dijk",
    "Kevin De Bruyne",
    "Harry Kane",
    "Florian Wirtz",
    "Jamal Musiala",
    "Federico Valverde",
    "Ferland Mendy",
    "Marquinhos",
    "Achraf Hakimi",
    "Gianluigi Donnarumma",

    # ── Légendes ──
    "Zinedine Zidane",
    "Ronaldo (joueur brésilien)",
    "Ronaldinho",
    "Thierry Henry",
    "Didier Drogba",
    "Andrés Iniesta",
    "Xavi Hernández",

    # ── Clubs ──
    "Paris Saint-Germain Football Club",
    "Real Madrid Club de Fútbol",
    "Manchester City Football Club",
    "FC Bayern Munich",
    "Arsenal Football Club",
    "FC Barcelone",
    "Liverpool FC",
    "Chelsea FC",
    "Juventus FC",
    "Inter Milan",
    "AC Milan",
    "Borussia Dortmund",
    "Olympique de Marseille",
    "Olympique lyonnais",
    "AS Monaco (football)",

    # ── Compétitions ──
    "Ligue des champions de l'UEFA 2024-2025",
    "Ligue des champions de l'UEFA 2023-2024",
    "Ligue 1 2024-2025",
    "Premier League 2024-2025",
    "Liga 2024-2025",
    "Serie A 2024-2025",
    "Ligue des champions de l'UEFA",
    "Coupe du monde de football 2022",
    "Coupe du monde de football 2018",
    "UEFA Euro 2024",
    "Copa América 2024",

    # ── Événements & récompenses ──
    "Finale de la Ligue des champions de l'UEFA 2025",
    "Finale de la Ligue des champions de l'UEFA 2024",
    "Ballon d'or 2024",
    "Ballon d'or 2023",

    # ── Sélections nationales ──
    "Équipe de France de football",
    "Équipe d'Espagne de football",
    "Équipe du Brésil de football",
    "Équipe d'Argentine de football",
    "Équipe d'Angleterre de football",
    "Équipe d'Allemagne de football",
    "Équipe du Portugal de football",

    # ── Histoire & culture foot ──
    "Histoire du football",
    "Championnat de France de football",
    "Coupe de France de football",
]


def fetch_article(title):
    page = wiki.page(title)
    if page.exists():
        return {
            "title": title,
            "text": page.text,
            "url": page.fullurl
        }
    print(f"  ⚠️  Article non trouvé : {title}")
    return None


def fetch_all(articles, output_path="wikipedia_football.json"):
    # Idempotence — si le fichier existe déjà on ne retélécharge pas
    if os.path.exists(output_path):
        print(f"✅ Déjà téléchargé — chargement depuis {output_path}")
        with open(output_path, "r", encoding="utf-8") as f:
            return json.load(f)

    data = []
    for title in tqdm(articles, desc="Téléchargement des articles Wikipedia"):
        article = fetch_article(title)
        if article:
            data.append(article)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(data)} articles téléchargés → {output_path}")
    return data


if __name__ == "__main__":
    data = fetch_all(ARTICLES)

    print(f"\n📊 Statistiques :")
    print(f"  Articles récupérés : {len(data)}")
    total_chars = sum(len(a['text']) for a in data)
    print(f"  Taille totale : {total_chars:,} caractères")
    print(f"\n📄 Aperçu — {data[0]['title']} :")
    print(data[0]['text'][:300])
