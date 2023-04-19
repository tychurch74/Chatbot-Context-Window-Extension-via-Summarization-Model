import json


def key_stop(input_string, json_filename="stop_words.json"):
    # Read the JSON file and store the words in a set for faster lookup
    with open(json_filename, "r") as f:
        word_dict = json.load(f)
    word_set = set(word_dict.keys())

    # Split the input string into words
    words = input_string.split()

    # Remove words from the input string if they are in the word_set
    filtered_words = [word for word in words if word.lower() not in word_set]

    # Combine the remaining words back into a string and return it
    return " ".join(filtered_words)
