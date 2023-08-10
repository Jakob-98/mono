# WIP...

import sqlite3
import faiss
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class VectorMetadata:
    vector: list
    file_path: str
    chunk_location: int  # Optional


class VectorDB(ABC):
    
    @abstractmethod
    def save_index(self, faiss_index):
        pass

    @abstractmethod
    def load_index(self):
        pass


class SL3VectorDB(VectorDB):
    
    def __init__(self, db_path='../persistence/vector_index.db'):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS faiss_indices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vector_data BLOB,
                file_path TEXT,
                chunk_location INTEGER
            )
            """)

    def save_index(self, faiss_index, metadata_list):
        # Assume metadata_list is a list of VectorMetadata instances, in the same order as vectors in the Faiss index.
        index_binary = faiss.serialize_index(faiss_index)
        for metadata in metadata_list:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("""
                INSERT INTO faiss_indices (vector_data, file_path, chunk_location) VALUES (?, ?, ?)
                """, (index_binary, metadata.file_path, metadata.chunk_location))

    def load_index(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT vector_data, file_path, chunk_location FROM faiss_indices ORDER BY id DESC")
        results = cursor.fetchall()
        
        if results:
            index_data = results[0][0]
            metadata_list = [VectorMetadata(vector=None, file_path=res[1], chunk_location=res[2]) for res in results]
            return faiss.deserialize_index(index_data), metadata_list
        return None, []


class FaissIndex:
    
    def __init__(self, dimension, persistence: VectorDB):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.persistence = persistence

    def add(self, data):
        """Add vectors to the index."""
        self.index.add(data)

    def search(self, queries, k):
        """Search for the top k nearest neighbors for each query."""
        return self.index.search(queries, k)

    def save(self):
        """Save the index using the persistence mechanism."""
        self.persistence.save_index(self.index)

    def load(self):
        """Load the latest index from the persistence mechanism."""
        loaded_index = self.persistence.load_index()
        if loaded_index:
            self.index = loaded_index

from sentence_transformers import SentenceTransformer
import numpy as np

class VectorSearchEngine:
    
    def __init__(self, embedding_model_name='paraphrase-distilroberta-base-v1', dimension=768, db_path='../persistence/vector_index.db'):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.faiss_index = FaissIndex(dimension, SL3VectorDB(db_path))
    
    def embed_text_file(self, file_path):
        """Convert a text file to an embedding."""
        with open(file_path, 'r') as f:
            text = f.read()
        return self.embedding_model.encode(text).reshape(1, -1)
    
    def add_to_index(self, file_path, chunk_location=None):
        """Add a file (or chunk) to the FAISS index and save its metadata."""
        embedding = self.embed_text_file(file_path)
        self.faiss_index.add(embedding)

        metadata = VectorMetadata(
            vector=embedding.tolist(),  # Convert numpy array to list for dataclass
            file_path=file_path,
            chunk_location=chunk_location
        )

        self.faiss_index.save([metadata])  # Wrap metadata in a list

    def search_nearest_neighbors(self, query_file, k=5):
        """Search for the top k nearest neighbors for a query file."""
        query_embedding = self.embed_text_file(query_file)
        distances, indices = self.faiss_index.search(query_embedding, k)
        
        _, metadata_list = self.faiss_index.persistence.load_index()
        results = [metadata_list[i] for i in indices[0]]

        return distances[0], results

# Usage Example
engine = VectorSearchEngine()
engine.add_to_index("file1.txt", chunk_location=0)  # Chunk_location can be an offset, or any other identifier for the part of the file.
engine.add_to_index("file2.txt", chunk_location=0)

distances, nearest_files_metadata = engine.search_nearest_neighbors("query_file.txt", 5)
for dist, metadata in zip(distances, nearest_files_metadata):
    print(f"Distance: {dist}, File: {metadata.file_path}, Chunk: {metadata.chunk_location}")
