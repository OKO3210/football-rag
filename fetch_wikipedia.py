import wikipediaapi
import json
import os
from tqdm import tqdm

wiki = wikipediaapi.Wikipedia(
    language="fr",
    user_agent="football-rag/1.0"
)

SAISONS = list(range(2008, 2026))


def generate_season_articles():
    articles = []

    for debut in SAISONS:
        fin = debut + 1
        saison = f"{debut}-{fin}"

        articles += [
            f"Championnat de France de football {saison}",
            f"Championnat d'Angleterre de football {saison}",
            f"Championnat d'Espagne de football {saison}",
            f"Championnat d'Italie de football {saison}",
            f"Championnat d'Allemagne de football {saison}",
            f"Ligue des champions de l'UEFA {saison}",
            f"Ligue Europa {saison}",
            f"Coupe de France de football {saison}",
            f"FA Cup {saison}",
        ]

    return articles


ARTICLES_FIXES = [
    # Joueurs actuels top niveau
    "Kylian Mbappé", "Vinicius Junior", "Jude Bellingham", "Erling Haaland",
    "Mohamed Salah", "Lamine Yamal", "Ousmane Dembélé", "Antoine Griezmann",
    "Lionel Messi", "Cristiano Ronaldo", "Neymar", "Pedri", "Gavi",
    "Rodri", "Toni Kroos", "Bukayo Saka", "Phil Foden", "Marcus Rashford",
    "Rúben Dias", "Virgil van Dijk", "Kevin De Bruyne", "Harry Kane",
    "Florian Wirtz", "Jamal Musiala", "Federico Valverde", "Marquinhos",
    "Achraf Hakimi", "Gianluigi Donnarumma", "Warren Zaïre-Emery",
    "Bradley Barcola", "Randal Kolo Muani", "João Neves", "Fabian Ruiz",
    "Lee Kang-in", "Vitinha", "Nuno Mendes", "Endrick",
    "Raphinha", "Robert Lewandowski", "Sadio Mané", "Karim Benzema",
    "Thibaut Courtois", "Alisson Becker", "Ederson", "Marc-André ter Stegen",
    "Casemiro", "Luka Modric", "Sergio Busquets", "Thiago Alcântara",
    "Raheem Sterling", "Leroy Sané", "Serge Gnabry", "Thomas Müller",
    "Kingsley Coman", "Benjamin Pavard", "Lucas Hernández",
    "Raphaël Varane", "Jules Koundé", "William Saliba", "Dayot Upamecano",
    "Aurélien Tchouaméni", "Matteo Guendouzi", "Adrien Rabiot",
    "Khvicha Kvaratskhelia", "Victor Osimhen", "Romelu Lukaku",
    "Nicolo Barella", "Alessandro Bastoni", "Milan Skriniar",
    "Theo Hernández", "Mike Maignan", "Olivier Giroud",
    "Christopher Nkunku", "Marcus Thuram", "Randal Kolo Muani",
    "Evan Ndicka", "Nordi Mukiele", "Gonçalo Ramos", "Desire Doué",

    # Légendes
    "Zinedine Zidane", "Ronaldo (joueur brésilien)", "Ronaldinho",
    "Thierry Henry", "Patrick Vieira", "Marcel Desailly", "Lilian Thuram",
    "Robert Pires", "Didier Deschamps", "Laurent Blanc", "Fabien Barthez",
    "Rivaldo", "Roberto Carlos", "Cafu", "Andrés Iniesta", "Xavi Hernández",
    "Carles Puyol", "David Villa", "Fernando Torres", "Iker Casillas",
    "Sergio Ramos", "Raúl González", "Roberto Baggio", "Paolo Maldini",
    "Francesco Totti", "Gianluigi Buffon", "Oliver Kahn", "Michael Ballack",
    "Miroslav Klose", "Philipp Lahm", "Bastian Schweinsteiger",
    "Steven Gerrard", "Frank Lampard", "John Terry", "Wayne Rooney",
    "Didier Drogba", "Samuel Eto'o", "Yaya Touré", "Michael Essien",
    "Jay-Jay Okocha", "Nwankwo Kanu", "George Weah",
    "Pelé", "Johan Cruyff", "Diego Maradona", "Franz Beckenbauer",
    "Michel Platini", "Marco van Basten", "Ruud Gullit",
    "Romário", "Bebeto", "Zico", "Sócrates",
    "Dennis Bergkamp", "Patrick Kluivert", "Clarence Seedorf",
    "Alessandro Del Piero", "Filippo Inzaghi", "Andrea Pirlo",
    "Zlatan Ibrahimović", "Henrik Larsson", "Freddie Ljungberg",

    # Clubs majeurs
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
    "Tottenham Hotspur Football Club",
    "Manchester United Football Club",
    "Newcastle United Football Club",
    "West Ham United Football Club",
    "Aston Villa Football Club",
    "Everton Football Club",
    "Leeds United Football Club",
    "Leicester City Football Club",
    "Wolverhampton Wanderers Football Club",
    "RB Leipzig",
    "Bayer Leverkusen",
    "VfB Stuttgart",
    "Eintracht Francfort",
    "Fiorentina",
    "Lazio Rome",
    "Atalanta Bergame",
    "Club Atlético de Madrid",
    "Real Betis Balompié",
    "Valencia CF",
    "Sporting CP",
    "RSC Anderlecht",
    "Club Bruges",
    "Celtic FC",
    "Rangers FC",

    # Competitions historiques et generales
    "Ligue des champions de l'UEFA",
    "Ligue Europa",
    "Ligue Europa Conférence",
    "Coupe du monde de football",
    "Championnat d'Europe de football de l'UEFA",
    "Copa América",
    "Coupe d'Afrique des nations",
    "Championnat de France de football",
    "Championnat d'Angleterre de football",
    "Championnat d'Espagne de football",
    "Championnat d'Italie de football",
    "Championnat d'Allemagne de football",
    "Trophée des champions",
    "Supercoupe d'Espagne de football",
    "Supercoupe de l'UEFA",
    "Coupe du monde des clubs de la FIFA",
    "Coupe de France de football",
    "FA Cup",
    "Coupe de la Ligue française de football",
    "DFB-Pokal",
    "Coppa Italia",
    "Copa del Rey",

    # Coupes du monde
    "Coupe du monde de football 1998",
    "Coupe du monde de football 2002",
    "Coupe du monde de football 2006",
    "Coupe du monde de football 2010",
    "Coupe du monde de football 2014",
    "Coupe du monde de football 2018",
    "Coupe du monde de football 2022",

    # Euros
    "Championnat d'Europe de football 2000",
    "Championnat d'Europe de football 2004",
    "Championnat d'Europe de football 2008",
    "Championnat d'Europe de football 2012",
    "Championnat d'Europe de football 2016",
    "Championnat d'Europe de football 2020",
    "UEFA Euro 2024",

    # Copa America
    "Copa América 2015",
    "Copa América 2016",
    "Copa América 2019",
    "Copa América 2021",
    "Copa América 2024",

    # CAN
    "Coupe d'Afrique des nations 2019",
    "Coupe d'Afrique des nations 2021",
    "Coupe d'Afrique des nations 2023",

    # Ballons d'or
    "Ballon d'or", "Ballon d'or 2018", "Ballon d'or 2019",
    "Ballon d'or 2021", "Ballon d'or 2022", "Ballon d'or 2023",
    "Ballon d'or 2024",

    # Selections nationales
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
    "Équipe de Belgique de football",
    "Équipe de Croatie de football",
    "Équipe du Danemark de football",

    # Histoire et culture
    "Histoire du football",
    "Statistiques et records du championnat de France de football",
    "Football",
    "Règles du football",
    "Transfert (football)",
    "Mercato",
    "VAR (football)",
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


def fetch_all():
    existing_data = []
    existing_titles = set()

    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        existing_titles = {article["title"] for article in existing_data}
        print(f"{len(existing_data)} articles deja presents.")

    all_targets = ARTICLES_FIXES + generate_season_articles()
    all_targets = list(dict.fromkeys(all_targets))

    to_fetch = [t for t in all_targets if t not in existing_titles]

    if not to_fetch:
        print("Tous les articles sont deja telecharges.")
        return existing_data

    print(f"{len(to_fetch)} nouveaux articles a telecharger...")

    new_data = []
    not_found = []

    for title in tqdm(to_fetch, desc="Telechargement Wikipedia"):
        article = fetch_article(title)
        if article:
            new_data.append(article)
        else:
            not_found.append(title)

    all_data = existing_data + new_data

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n{len(new_data)} nouveaux articles ajoutes.")
    print(f"{len(not_found)} articles non trouves : {not_found[:10]}{'...' if len(not_found) > 10 else ''}")
    print(f"Total : {len(all_data)} articles")

    return all_data


if __name__ == "__main__":
    data = fetch_all()
    total_chars = sum(len(a["text"]) for a in data)
    print(f"\nStatistiques :")
    print(f"  Articles : {len(data)}")
    print(f"  Taille totale : {total_chars:,} caracteres")
