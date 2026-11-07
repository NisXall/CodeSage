import chromadb
from pathlib import Path

db_path = Path("./test_chroma").resolve()

print("Database path:", db_path)
print("ChromaDB version:", chromadb.__version__)

client = chromadb.PersistentClient(
    path=str(db_path)
)

print("Client initialized!")
print("Collections:", client.list_collections())