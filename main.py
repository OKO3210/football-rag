from groq import Groq
from dotenv import load_dotenv
import os

from vector_db import VectorDB
from config import LLM_MODEL_NAME, VECTOR_DB_NAME, CONTEXT_FILE, N_CHUNKS


class RAG:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.vector_db_object = VectorDB(VECTOR_DB_NAME)
        self.context = self._read_file(CONTEXT_FILE)

    @staticmethod
    def _read_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def build_context(self, question):
        chunks, metadatas = self.vector_db_object.retrieve(question, n=N_CHUNKS)

        formatted_chunks = ""
        for chunk, metadata in zip(chunks[0], metadatas[0]):
            formatted_chunks += (
                f"\n[Source : {metadata['source']} | {metadata['url']}]\n{chunk}\n"
            )

        return self.context.replace("{{Chuncks}}", formatted_chunks)

    def answer_question(self, question):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.build_context(question),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
            model=LLM_MODEL_NAME,
        )
        return chat_completion.choices[0].message.content


def main():
    rag_object = RAG()
    print("ParisBot pret ! Tape 'exit' pour quitter.\n")

    while True:
        question = input("Toi : ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            print("A bientot !")
            break
        response = rag_object.answer_question(question)
        print(f"\nParisBot : {response}\n")


if __name__ == "__main__":
    main()
