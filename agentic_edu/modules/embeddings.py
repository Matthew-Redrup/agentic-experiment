from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel


class DatabaseEmbedder:   
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.map_name_to_embeddings = {}
        self.map_name_to_table_def = {}
        
    def add_table(self, table_name: str, text_representation: str):
        self.map_name_to_embeddings[table_name] = self.compute_embeddings(
            text_representation
        )
        
        self.map_name_to_table_def[table_name] = text_representation
        
    def compute_embeddings(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )
        outputs = self.model(**inputs)
        return outputs["pooler_output"].detach().numpy()
    
    def get_similar_tables_via_embeddings(self,query, n=3):
        query_embedding = self.compute_embeddings(query)
        similarities = {}
        for table_name, table_embedding in self.map_name_to_embeddings.items():
            similarities[table_name] = cosine_similarity(
                query_embedding, table_embedding
            )[0][0]
            
        return sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:n]