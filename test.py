from src.modules.text_summarization import Summarizer


message_history = [{"role": "system", "content": "You are a chatbot that gives short, concise responses based on the following context"},    
                    {"role": "user", "content": "Good morning, how would I combine 'content' from the following code into a single string?:"},    
                    {"role": "assistant", "content": "In this code, we first define inp and message_history as in the original code. We then use a list comprehension to extract the values of the content keys from each dictionary in message_history, and store them in the content list. To combine these strings into a single string, we use the join() method, which takes an iterable (in this case, the content list) and joins all of its elements together into a single string, using the string that join() was called on as a separator. Since we want to combine the strings without any separators, we pass an empty string to join(). Finally, we print the combined_content string, which should be the concatenation of the content strings from the three dictionaries in message_history."}
                    ]


def conversation_sum(message_history):
    if not message_history:
        conversation_summary = [{"role": "system", "content": "You are a chatbot that gives short, concise responses based on the following context (no conversation history yet)"}]
        
    else:
        content = [message["content"] for message in message_history]
        combined_content = "".join(content)

        summarizer = Summarizer()
        corrected = summarizer.process_in_chunks(combined_content, chunk_size=4)

        conversation_summary = [{"role": "system", "content": f"You are a chatbot that gives short, concise responses based on the following context {corrected}"}]

    return(conversation_summary)

