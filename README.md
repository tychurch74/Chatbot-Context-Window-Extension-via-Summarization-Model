# Chatbot Context Window Extension via Summarization Model
*To view results navigate to the 'testing_data' folder. There you will find text conversation transcripts as well as JSON data containing the full output from the OpenAI API and the entire conversation history.*

This set of Python scripts uses OpenAI's GPT-3.5-turbo language model to create a chatbot that provides short, concise responses based on the context of the conversation. It includes a conversation summarization feature utilizing a fine tuned version of Google's BART LLM that allows the chatbot to retain a summary of previous interactions, partially simulating long-term memory, even for lengthy conversations. In addition to summarization there is also a simple key-word search mechanism that allows the model to gain specific contextual information based on key-words within a user's prompt.

## Problem
Chatbots utilizing LLM's such as ChatGPT have a limited token count, restricting the context window size. If the conversation grows too long, the context window will truncate the conversation, causing the chatbot to lose prior interactions' context. By using a conversation summarizer and inserting it's output within OpenAI's newly implemented 'system message', the chatbot can maintain a summarized context of the entire conversation, keeping the token count within acceptable limits and simulating a kind of 'long-term memory'.

## Possible Improvements
- Implement an additional 'attention mechanism' within the summarizer module to focus on the most important parts of the conversation. This could be done by using a custom attention layer within the summarizer, or by using a pre-trained attention mechanism such as BERT.
- Improve the summarizer's output speed by using a GPU and/or by running the summarization process in parallel with the chatbot API call.
- Investigate how open source chat bots such as Llamma-7B, GPT-j or FLAN-T5 perform with this method.

## How to Use
1. Install the required dependencies:

```
pip install openai
pip install nltk
pip install transformers
pip install torch
pip install pandas
pip install pillow
pip install elevenlabslib
pip install pydub
```

2. Navigate to src/main.py (terminal based) or src/gui.py (GUI app) and add your OpenAI API key to your environment variables as per the instructions here: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

3. Modify the settings at the beginning of the code as required, such as the num_iterations, chunk_size, completion_file_path, and message_history_file_path.

4. Run the script in your terminal or through basic GUI app.

5. Enter your input when prompted. The chatbot will provide responses based on the context of the summarized conversation.

6. The conversation data will be logged into JSON files specified by the completion_file_path and message_history_file_path settings if enable_json_output is set to True.


## Settings
You can modify the following settings in the script:

enable_json_output: A boolean value to enable or disable JSON file outputs (False by default).

num_iterations: The number of user inputs the script will accept in the main loop. This setting is merely a safety measure to prevent a user from inadvertantly racking up substantial API costs. Change this value to anything that suits your API budget.

chunk_size: The number of sentences fed into the summarizer at a time, increase this value if you intend of having extremely long conversations (4 by default).

completion_file_path: The file path for the completion.json file. This file will contain the full output from the OpenAI API and the last set of system messages.

message_history_file_path: The file path for the message_history.json file. This file will contain the entire conversation history from beginning to end.


## Custom modules:
modules.text_summarization: A custom text summarization module.

modules.chatGPT: Module for interacting with the OpenAI API with custom functionality.

modules.stop_words: Removes list of most common English words from key-word string to avoid the keyword search from returning nearly every response within the conversation history.

modules.key_word_search: A custom key-word search module.

modules.io_utils: Custom I/O utility functions for JSON files.