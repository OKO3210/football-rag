import wikipediaapi
import json
import os
from tqdm import tqdm

wiki = wikipediaapi.Wikipedia(
    language="fr",
    user_agent="football-rag/1.0"
)

ARTICLES = [
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
    "Gavi",
    "Rodri",
    "Toni Kroos",
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
    "Marquinhos",
    "Achraf Hakimi",
    "Gianluigi Donnarumma",
    "Warren Zaïre-Emery",
    "Bradley Barcola",
    "Randal Kolo Muani",
    "João Neves",
    "Fabian Ruiz",
    "Lee Kang-in",
    "Vitinha",
    "Nuno Mendes",
    "Nordi Mukiele",
    "Willian Pacho",
    "Matvey Safonov",
    "Alexandre Lacazette",
    "Pierre-Emerick Aubameyang",
    "Didier Drogba",
    "Samuel Eto'o",
    "Ronaldinho",
    "Zinedine Zidane",
    "Thierry Henry",
    "Patrick Vieira",
    "Marcel Desailly",
    "Lilian Thuram",
    "Robert Pires",
    "Ronaldo (joueur brésilien)",
    "Rivaldo",
    "Roberto Carlos",
    "Cafu",
    "Andrés Iniesta",
    "Xavi Hernández",
    "Carles Puyol",
    "Victor Valdés",
    "David Villa",
    "Fernando Torres",
    "Iker Casillas",
    "Sergio Ramos",
    "Raúl González",
    "Roberto Baggio",
    "Paolo Maldini",
    "Francesco Totti",
    "Gianluigi Buffon",
    "Oliver Kahn",
    "Michael Ballack",
    "Miroslav Klose",
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
    "Borussia Mönchengladbach",
    "Atlético de Madrid",
    "Séville FC",
    "Real Sociedad",
    "Villarreal CF",
    "SSC Naples",
    "AS Roma",
    "SL Benfica",
    "FC Porto",
    "Ajax Amsterdam",
    "Olympique de Marseille",
    "Olympique lyonnais",
    "AS Monaco (football)",
    "LOSC Lille",
    "OGC Nice",
    "Stade rennais Football Club",
    "RC Lens",
    "Girondins de Bordeaux",
    "AS Saint-Étienne",
    "FC Nantes",
    "Ligue des champions de l'UEFA 2024-2025",
    "Ligue des champions de l'UEFA 2023-2024",
    "Ligue des champions de l'UEFA 2022-2023",
    "Ligue des champions de l'UEFA 2020-2021",
    "Ligue des champions de l'UEFA 2018-2019",
    "Ligue des champions de l'UEFA",
    "Ligue 1 2024-2025",
    "Ligue 1 2023-2024",
    "Championnat de France de football",
    "Premier League 2023-2024",
    "Premier League",
    "Liga 2023-2024",
    "Championnat d'Espagne de football",
    "Serie A 2023-2024",
    "Championnat d'Italie de football",
    "Bundesliga 2023-2024",
    "Championnat d'Allemagne de football de football",
    "UEFA Euro 2024",
    "UEFA Euro 2020",
    "Coupe du monde de football 2022",
    "Coupe du monde de football 2018",
    "Coupe du monde de football 2014",
    "Coupe du monde de football 2006",
    "Coupe du monde de football 1998",
    "Copa América 2024",
    "Copa América 2021",
    "Ligue Europa 2023-2024",
    "Ligue Europa UEFA",
    "Ligue Europa Conférence 2023-2024",
    "Supercoupe de l'UEFA 2024",
    "Ballon d'or 2024",
    "Ballon d'or 2023",
    "Ballon d'or 2022",
    "Ballon d'or 2021",
    "Ballon d'or",
    "Équipe de France de football",
    "Équipe d'Espagne de football",
    "Équipe du Brésil de football",
    "Équipe d'Argentine de football",
    "Équipe d'Angleterre de football",
    "Équipe d'Allemagne de football",
    "Équipe du Portugal de football",
    "Équipe d'Italie de football",
    "Équipe des Pays-Bas de football",
    "Équipe du Maroc de football",
    "Équipe du Sénégal de football",
    "Histoire du football",
    "Coupe de France de football",
    "Trophée des champions",
    "Supercoupe d'Espagne de football",
    "Coupe du monde des clubs de la FIFA",
]

OUTPUT_PATH = "wikipedia_football.json"


def fetch_article(title):
    page = wiki.page(title)
    if page.exists():
        return {
            "title": title,
            "text": page.text,
            "url": page.fullurl
        }
    return None


def fetch_all(articles, output_path=OUTPUT_PATH):
    existing_data = []
    existing_titles = set()

    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        existing_titles = {article["title"] for article in existing_data}
        print(f"{len(existing_data)} articles deja presents.")

    articles_to_fetch = [title for title in articles if title not in existing_titles]

    if not articles_to_fetch:
        print("Tous les articles sont deja telecharges.")
        return existing_data

    print(f"{len(articles_to_fetch)} nouveaux articles a telecharger...")

    new_data = []
    for title in tqdm(articles_to_fetch, desc="Telechargement Wikipedia"):
        article = fetch_article(title)
        if article:
            new_data.append(article)
        else:
            print(f"  Article non trouve : {title}")

    all_data = existing_data + new_data

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n{len(new_data)} nouveaux articles ajoutes.")
    print(f"Total : {len(all_data)} articles -> {output_path}")

    return all_data


if __name__ == "__main__":
    data = fetch_all(ARTICLES)

    total_chars = sum(len(article["text"]) for article in data)
    print(f"\nStatistiques :")
    print(f"  Articles : {len(data)}")
    print(f"  Taille totale : {total_chars:,} caracteres")
    print(f"\nApercu - {data[0]['title']} :")
    print(data[0]["text"][:300])
