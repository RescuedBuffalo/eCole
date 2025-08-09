import os
import sqlite3
import uuid
from typing import List, Dict

from chromadb import Client
from chromadb.config import Settings

DB_PATH = os.environ.get("ECOLE_DB_PATH", "ecole/data/events.db")
CHROMA_PATH = os.environ.get("ECOLE_CHROMA_PATH", "ecole/data/chroma")

_conn = None
_client = None
_collection = None


class DummyEmbeddingFunction:
    def __call__(self, texts):
        return [[float(len(t))] for t in texts]


def _get_conn():
    global _conn
    if _conn is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _conn = sqlite3.connect(DB_PATH)
        _conn.execute(
            "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, intent TEXT, emotion TEXT, timestamp TEXT)"
        )
    return _conn


def _get_collection():
    global _client, _collection
    if _client is None:
        os.makedirs(CHROMA_PATH, exist_ok=True)
        _client = Client(
            Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_PATH)
        )
        _collection = _client.get_or_create_collection(
            "events", embedding_function=DummyEmbeddingFunction()
        )
    return _collection


def write_event(event: Dict[str, str]) -> None:
    conn = _get_conn()
    conn.execute(
        "INSERT INTO events(content,intent,emotion,timestamp) VALUES (?,?,?,?)",
        (event["content"], event["intent"], event["emotion"], event["timestamp"]),
    )
    conn.commit()
    collection = _get_collection()
    collection.add(
        documents=[event["content"]],
        metadatas=[{"intent": event["intent"], "emotion": event["emotion"], "timestamp": event["timestamp"]}],
        ids=[str(uuid.uuid4())],
    )


def retrieve_recent(k: int) -> List[Dict[str, str]]:
    conn = _get_conn()
    cursor = conn.execute(
        "SELECT content,intent,emotion,timestamp FROM events ORDER BY id DESC LIMIT ?",
        (k,),
    )
    rows = cursor.fetchall()
    return [
        {"content": c, "intent": i, "emotion": e, "timestamp": t} for c, i, e, t in rows
    ]


def search_memory(query: str, k: int = 3) -> List[str]:
    collection = _get_collection()
    result = collection.query(query_texts=[query], n_results=k)
    return result.get("documents", [[]])[0]
