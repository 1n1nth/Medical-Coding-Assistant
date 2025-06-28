import spacy
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class MedicalCoder:
    def __init__(self, csv_path, index_path, embeddings_path):
        # Load models
        self.nlp = spacy.load("en_core_web_sm")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load data
        self.df = pd.read_csv(csv_path)
        self.index = faiss.read_index(index_path)
        self.description_embeddings = np.load(embeddings_path)
        
        print("Models and data loaded successfully")
        
    def normalize_input(self, text):
        doc = self.nlp(text.lower())
        keywords = [ent.text for ent in doc.ents]
        return ' '.join(keywords) if keywords else text.lower()
        
    def suggest_codes(self, user_input, top_n=10):
        normalized = self.normalize_input(user_input)
        print(f"Normalized input: {normalized}")
        
        # Encode the input text
        input_embedding = self.embedder.encode(normalized, convert_to_tensor=True).cpu().numpy().reshape(1, -1)
        
        # Search for similar codes using FAISS
        D, I = self.index.search(input_embedding, top_n)

        results = []
        for i, idx in enumerate(I[0]):
            if idx < len(self.df):  # Safeguard against index out of bounds
                code = self.df.at[idx, 'code']
                formatted_code = code[:3] + '.' + code[3:] if len(code) > 3 else code
                results.append({
                    "code": code,
                    "formatted_code": formatted_code,
                    "description": self.df.at[idx, 'description'],
                    "score": round(float(D[0][i]), 3)
                })
        
        # Sort results by score in descending order
        results.sort(key=lambda x: x["score"], reverse=True)
        
        print(f"Found {len(results)} matching codes")
        return results
    
    