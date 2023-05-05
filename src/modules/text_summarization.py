import tiktoken
import nltk

from transformers import pipeline


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def summary(text, max_length=64, min_length=16, do_sample=False):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    output = summarizer(
        text, max_length=max_length, min_length=min_length, do_sample=do_sample
    )
    summary = output[0]["summary_text"]
    return summary


def split_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences


def process_in_chunks(text, chunk_size=8):
    sentences = split_sentences(text)
    combined_summary = []
    for i in range(0, len(sentences), chunk_size):
        chunk = sentences[i : i + chunk_size]
        combined_sentences = " ".join(chunk)
        chunk_summary = summary(combined_sentences)
        combined_summary.append(chunk_summary)
        joined_summary = " ".join(combined_summary)
    return joined_summary


# Note to self: This function is the dominant time complexity in the program at O(n^3 * log(n))... I think.
def iterative_summary(
    input_text,
    max_tokens,
    summary_function=process_in_chunks,
    token_count_function=num_tokens_from_string,
):
    if token_count_function(input_text) <= max_tokens:
        current_summary = input_text

    else:
        current_summary = summary_function(input_text)

        while token_count_function(current_summary) > max_tokens:
            current_summary = summary_function(current_summary)

    return current_summary
