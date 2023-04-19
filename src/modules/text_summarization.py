from transformers import pipeline
import nltk

nltk.download("punkt")


class Summarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=model_name)

    def summary(self, text, max_length=64, min_length=16, do_sample=False):
        output = self.summarizer(
            text, max_length=max_length, min_length=min_length, do_sample=do_sample
        )
        summary = output[0]["summary_text"]
        return summary

    def split_sentences(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    def process_in_chunks(self, text, chunk_size):
        sentences = self.split_sentences(text)
        combined_summary = []
        for i in range(0, len(sentences), chunk_size):
            chunk = sentences[i : i + chunk_size]
            combined_sentences = " ".join(chunk)
            chunk_summary = self.summary(combined_sentences)
            combined_summary.append(chunk_summary)
            summary_length = len(combined_summary)
        joined_summary = " ".join(combined_summary)
        if summary_length > 8:
            final_summary = self.summary(joined_summary, max_length=256, min_length=64)
        else:
            final_summary = joined_summary
        return final_summary
