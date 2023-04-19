import openai

from modules.text_summarization import Summarizer
from modules.io_utils import write_json, json_obj
from modules.stop_words import key_stop


class ChatGPT:
    def __init__(
        self,
        openai_api_key,
        enable_json_output=False,
        chunk_size=4,
        completion_file_path="data/completion.json",
    ):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        self.enable_json_output = enable_json_output
        self.chunk_size = chunk_size
        self.completion_file_path = completion_file_path
        self.message_history = []

    def generate_conversation_summary(self):
        if not self.message_history:
            conversation_summary = [
                {
                    "role": "system",
                    "content": "You are a chatbot that gives short, concise responses based on the following context: (no conversation history yet)",
                }
            ]
        else:
            content = [message["content"] for message in self.message_history]
            combined_content = "".join(content)
            summarizer = Summarizer()
            summary = summarizer.process_in_chunks(
                combined_content, chunk_size=self.chunk_size
            )
            conversation_summary = [
                {
                    "role": "system",
                    "content": f"You are a chatbot that gives short, concise responses based on the following context: {summary}",
                }
            ]

        return conversation_summary

    def keyword_search(self, input_string):
        related_messages = []
        message_key = key_stop(input_string)
        keywords = message_key.split()
        for message in self.message_history:
            for keyword in keywords:
                if keyword.lower() in message["content"].lower():
                    related_messages.append(message)
                    break  # No need to check for other keywords, one match is enough

        related_content = [message["content"] for message in related_messages]
        return related_content

    def chat(self, inp, role="user"):
        conversation_summary = self.generate_conversation_summary()
        if not self.message_history:
            related_content = "no conversation history yet"
        else:
            related_content = self.keyword_search(inp)
        conversation_summary.append(
            {
                "role": "system",
                "content": f"here is some additional context from past messages: {related_content}",
            }
        )
        conversation_summary.append(
            {"role": role, "content": f"based on the context given {inp}"}
        )
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=conversation_summary
        )
        chat_data = json_obj(conversation_summary, completion)
        if self.enable_json_output:
            write_json(chat_data, self.completion_file_path)
        else:
            pass
        reply_content = completion.choices[0].message.content
        self.message_history.append({"role": "assistant", "content": reply_content})
        return reply_content
