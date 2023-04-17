from transformers import pipeline
import json
import nltk

nltk.download('punkt')

class Summarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=model_name)

    def summary(self, text):
        output = self.summarizer(text, max_length=64, min_length=16, do_sample=False)
        summary = output[0]['summary_text']
        return summary

    def split_sentences(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    def process_in_chunks(self, text, chunk_size):
        sentences = self.split_sentences(text)
        combined_summary = []
        for i in range(0, len(sentences), chunk_size):
            chunk = sentences[i:i+chunk_size]
            combined_sentences = ' '.join(chunk)
            chunk_summary = self.summary(combined_sentences)
            combined_summary.append(chunk_summary)
        final_summary = ' '.join(combined_summary)
        return final_summary













