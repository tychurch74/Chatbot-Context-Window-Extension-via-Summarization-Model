
from sentence_transformers import SentenceTransformer, util
import torch
import nltk

class SemanticSearch:
    def __init__(self, message_history):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.message_history = message_history
        self.corpus = self.get_corpus()

    def get_corpus(self):
        content = [message["content"] for message in self.message_history]
        corpus = []
        for i in range(len(content)):
            sentence = nltk.sent_tokenize(content[i])
            corpus.extend(sentence)

        return corpus

    def semantic_search(self, query, top_k=5):
        corpus_embeddings = self.embedder.encode(self.corpus, convert_to_tensor=True)

        top_k = min(top_k, len(self.corpus))

        query_embedding = self.embedder.encode(query, convert_to_tensor=True)

        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)
        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            results.append(self.corpus[idx])

        relevant_sentences = "".join(results)

        return relevant_sentences
    
