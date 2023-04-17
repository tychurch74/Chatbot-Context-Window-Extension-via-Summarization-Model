# GPT-3.5-turbo Chatbot with Conversation Summarization
This Python script uses OpenAI's GPT-3.5-turbo language model to create a chatbot that provides short, concise responses based on the context of the conversation. It includes a conversation summarization feature that allows the chatbot to retain a summary of previous interactions and simulate long-term memory, even for lengthy conversations.

## Problem
Chatbots utilizing GPT-3.5-turbo have a limited token count, restricting the context window size. If the conversation grows too long, the context window will truncate the conversation, causing the chatbot to lose prior interactions' context. By using a conversation summarizer, the chatbot can maintain a summarized context, keeping the token count within acceptable limits and simulating long-term memory.

## How to Use
1. Install the required dependencies:

```
pip install openai
pip install nltk
pip install transformers
pip install torch
pip install pandas
pip install pillow
```

2. Navigate to src/main.py and add your OpenAI API key to the openai.api_key setting. Implement a secure method to store and load your API key.

3. Modify the settings at the beginning of the code as required, such as the num_iterations, chunk_size, completion_file_path, and message_history_file_path.

4. Run the script in your terminal.

5. Enter your input when prompted. The chatbot will provide responses based on the context of the summarized conversation.

6. The conversation data will be logged into JSON files specified by the completion_file_path and message_history_file_path settings if enable_json_output is set to True.


## Settings
You can modify the following settings in the script:

openai.api_key: Your OpenAI API key (implement a secure method to load this value).

enable_json_output: A boolean value to enable or disable JSON file outputs (True by default).

num_iterations: The number of user inputs the script will accept in the main loop (3 by default).

chunk_size: The size of chunks for the Summarizer (4 by default).

completion_file_path: The file path for the completion.json file.

message_history_file_path: The file path for the message_history.json file.


## Custom modules:
modules.text_summarization: A custom text summarization module.

data.io_utils: Custom I/O utility functions for JSON files.