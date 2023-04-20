from transformers import pipeline
import nltk

nltk.download("punkt")


class Summarizer:
    """
    A class that performs text summarization using the BART model from Hugging Face.

    Attributes:
        summarizer (Pipeline): A Hugging Face summarization pipeline object.
    """

    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initializes a new instance of the Summarizer class.

        Args:
            model_name (str, optional): The name of the BART model to use. Defaults to "facebook/bart-large-cnn".

        """
        self.summarizer = pipeline("summarization", model=model_name)

    def summary(self, text, max_length=64, min_length=16, do_sample=False):
        """
        Generates a summary of the given text.

        Args:
            text (str): The text to be summarized.
            max_length (int, optional): The maximum length of the summary. Defaults to 64.
            min_length (int, optional): The minimum length of the summary. Defaults to 16.
            do_sample (bool, optional): Whether or not to use sampling to generate the summary. Defaults to False.

        Returns:
            A string representing the summary of the given text.

        """
        output = self.summarizer(
            text, max_length=max_length, min_length=min_length, do_sample=do_sample
        )
        summary = output[0]["summary_text"]
        return summary

    def split_sentences(self, text):
        """
        Splits the given text into sentences.

        Args:
            text (str): The text to be split into sentences.

        Returns:
            A list of sentences extracted from the given text.

        """
        sentences = nltk.sent_tokenize(text)
        return sentences

    def process_in_chunks(self, text, chunk_size):
        """
        Generates a summary of the given text by processing it in chunks. If the number of sentences in summary is greater than 8, then the summary is further processed to reduce the length.

        Args:
            text (str): The text to be summarized.
            chunk_size (int): The number of sentences to process at a time.

        Returns:
            A string representing the summary of the given text.

        """
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