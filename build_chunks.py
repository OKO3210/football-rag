import json
import os

CHUNK_SIZE = 500
OVERLAP = 100


def chunk_article(article, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Decoupe un article Wikipedia en chunks de taille fixe avec overlap.
    Chaque chunk est prefixe par le titre de l'article pour que le LLM
    sache toujours de qui/quoi on parle.
    """
    title = article["title"]
    url = article["url"]
    words = article["text"].split()

    chunks = []
    metadatas = []

    word_index = 0
    while word_index < len(words):
        chunk_words = words[word_index : word_index + chunk_size]
        chunk_text = f"[{title}] " + " ".join(chunk_words)

        chunks.append(chunk_text)
        metadatas.append({"source": title, "url": url})

        word_index += chunk_size - overlap

    return chunks, metadatas


def build_all_chunks(json_path="wikipedia_football.json"):
    """
    Charge le JSON Wikipedia et construit tous les chunks + metadonnees.
    Idempotence : si le fichier chunks existe deja, on le charge directement.
    """
    output_path = "chunks_football.json"

    if os.path.exists(output_path):
        print(f"Chunks deja construits - chargement depuis {output_path}")
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["chunks"], data["metadatas"]

    print(f"Chargement des articles depuis {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    all_chunks = []
    all_metadatas = []

    for article in articles:
        chunks, metadatas = chunk_article(article)
        all_chunks.extend(chunks)
        all_metadatas.extend(metadatas)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {"chunks": all_chunks, "metadatas": all_metadatas},
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"{len(all_chunks)} chunks construits depuis {len(articles)} articles")
    print(f"Sauvegarde dans {output_path}")

    return all_chunks, all_metadatas


if __name__ == "__main__":
    chunks, metadatas = build_all_chunks()

    print(f"\nStatistiques :")
    print(f"   Total chunks : {len(chunks)}")
    print(f"   Sources uniques : {len(set(m['source'] for m in metadatas))}")

    print(f"\nExemple de chunk :")
    print(chunks[0][:300])
    print(f"\nMetadonnee associee :")
    print(metadatas[0])
