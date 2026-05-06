from sentence_transformers import SentenceTransformer
import chromadb
from config import EMBEDDING_MODEL_NAME
from build_chunks import build_all_chunks
import os


class VectorDB:
	def __init__(self, vector_db_name, chunks=None, metadatas=None):

		if os.path.exists(vector_db_name):
			self.load_vector_db(vector_db_name)

		elif chunks:
			self.create_vector_db(vector_db_name, chunks, metadatas)

		else:
			raise Exception("Can't initiate vector db object ! please give a path to a vector db or chunks.")


	def create_vector_db(self, vector_db_name, chunks, metadatas=None):
		print("Creation de la base de donnees vectorielle...")
		print(f"Embedding model : {EMBEDDING_MODEL_NAME}")

		self.sentence_transformer_object = SentenceTransformer(EMBEDDING_MODEL_NAME)
		self.chroma = chromadb.PersistentClient(path=vector_db_name)

		collection = self.chroma.get_or_create_collection(
			name="knowledge",
			metadata={"embedding_model": EMBEDDING_MODEL_NAME}
		)

		embeddings = self.get_embeddings(chunks)

		# Si pas de metadonnees fournies, on cree des metadonnees vides
		if metadatas is None:
			metadatas = [{"source": "unknown"} for _ in range(len(chunks))]

		collection.add(
			ids=[f"chunk_{chunk_index}" for chunk_index in range(len(chunks))],
			documents=chunks,
			embeddings=embeddings,
			metadatas=metadatas
		)

		print(f"{len(chunks)} chunks indexes dans la base de donnees.")


	def load_vector_db(self, vector_db_name):
		print("Chargement de la base de donnees vectorielle...")
		self.chroma = chromadb.PersistentClient(path=vector_db_name)
		collection_info = self.chroma.get_collection("knowledge")
		embedding_model = collection_info.metadata["embedding_model"]
		print(f"Embedding model : {embedding_model}")
		self.sentence_transformer_object = SentenceTransformer(embedding_model)


	def get_embeddings(self, chunks):
		embeddings = self.sentence_transformer_object.encode(
			chunks,
			batch_size=64,
			normalize_embeddings=True,
			show_progress_bar=True
		).tolist()
		return embeddings


	def retrieve(self, question, n=3):
		embedded_question = self.get_embeddings([question])[0]
		collection = self.chroma.get_or_create_collection("knowledge")
		results = collection.query(query_embeddings=[embedded_question], n_results=n)
		return results["documents"], results["metadatas"]


if __name__ == "__main__":
	chunks, metadatas = build_all_chunks()
	vector_db_object = VectorDB(
		vector_db_name="football_knowledge",
		chunks=chunks,
		metadatas=metadatas
	)
	print("Base de donnees vectorielle football prete !")
