import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Using a lightweight model for the sandbox to avoid memory issues
        self.model = SentenceTransformer(model_name)
        self.facts_path = os.path.join(os.path.dirname(__file__), "verified_facts.json")
        self.facts = self.load_facts()
        self.index = None
        self.build_index()

    def load_facts(self):
        with open(self.facts_path, 'r') as f:
            return json.load(f)

    def build_index(self):
        texts = [f['text'] for f in self.facts]
        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query, top_k=2):
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            fact = self.facts[idx]
            # Convert L2 distance to a simple similarity score (approximate)
            similarity = 1 / (1 + dist)
            results.append({
                "fact": fact,
                "similarity": similarity
            })
        return results

# Singleton instance
store = None

def get_vector_store():
    global store
    if store is None:
        store = VectorStore()
    return store
