from pathlib import Path
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import plotly.express as px
import pandas as pd
from PIL import Image
import base64
import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


cwd = os.getcwd()

dir_path = cwd + "/logs/"
if os.path.exists(dir_path):
    pass
else:
    os.mkdir(dir_path)


class APIClient:
    def __init__(self, model="gpt-4o-mini", resp_form={"type":"text"}, t=1, max_t=2048, top_p=1, freq=0, pre_p=0):
        self.model = model
        self.resp_form = resp_form
        self.t = t
        self.max_t = max_t
        self.top_p = top_p
        self.freq = freq
        self.pre_p = pre_p

    def send_message(self, messages, parse_content=True):
        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format=self.resp_form,
            temperature=self.t,
            max_completion_tokens=self.max_t,
            top_p=self.top_p,
            frequency_penalty=self.freq,
            presence_penalty=self.pre_p
        )
        return completion.choices[0].message.content if parse_content else completion

class Message:
    def __init__(self):
        self.content = []
    
    def add_text(self, text):
        self.content.append({
            "type": "text",
            "text": text
        })
        return self
    
    def add_image(self, image_path):
        encoded = self._encode_image(image_path)
        self.content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
        })
        return self
    
    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def build(self, role):
        return {
            "role": role,
            "content": self.content
        }

class ProcessResponse:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self._init_file()
    
    def _init_file(self):
        self.timestamp = str(datetime.datetime.now())
        self.filename = self.timestamp.split(".")[1] + ".txt"
    
    def log_conversation(self, messages, counter):
        # Log raw conversation data to logs.txt
        log_text = f"{counter} | {self.timestamp}\n\n{str(messages)}\n\n---\n\n"
        self._write_file("logs.txt", log_text)
        
        # Log readable conversation to conversation record file
        latest_message = messages[-1]
        record_text = self._format_message(latest_message, counter)
        self._write_file(self.filename, record_text)
    
    def _format_message(self, message, counter):
        formatted = f"\n{counter} | {self.timestamp}\n"
        role = message['role'].capitalize()
        content = message['content']
        
        if isinstance(content, list):
            # Handle structured content (text/image)
            text_content = []
            for item in content:
                if item['type'] == 'text':
                    text_content.append(item['text'])
            content = '\n'.join(text_content)
        
        return f"{formatted}{role}:\n{content}\n\n---\n"
    
    def _write_file(self, filename, content):
        with open(f"{self.dir_path}{filename}", "a") as f:
            f.write(content)

class ChatThread:
    def __init__(self, model="gpt-4o-mini", response_format={"type":"text"}, dir_path=None):
        self.messages = []
        self.counter = 0
        self.api_client = APIClient(model=model, resp_form=response_format)
        self.processor = ProcessResponse(dir_path) if dir_path else None
    
    def add_message(self, role, content_builder):
        message = content_builder(Message())
        formatted = message.build(role)
        self.messages.append(formatted)
        
        if self.processor:
            self.counter += 1
            self.processor.log_conversation(self.messages, self.counter)
        
        return self
    
    def get_context(self):
        return self.messages.copy()
    
    def send(self):
        response_content = self.api_client.send_message(self.messages)
        if not response_content:
            return None
            
        assistant_message = {"role": "assistant", "content": response_content}
        self.messages.append(assistant_message)
        
        if self.processor:
            self.counter += 1
            self.processor.log_conversation(self.messages, self.counter)
        
        return response_content
    
    def text_message(self, role="user", content=""):
        self.add_message(role, lambda m: m.add_text(content))

    def attach_image(self, path_to_image):
        self.add_message("user", lambda m: m.add_image(path_to_image))

class AINotes:
    def __init__(self):
        self.thread = ChatThread(model="gpt-4o-mini", dir_path=None)

    def dev_chat(self,d):
        self.thread.text_message(role="developer", content=d)

    def chat(self,m):
        self.thread.text_message(role="user", content=m)
        response = self.thread.send()
        print(response)

    def image_chat(self, m, i):
        self.thread.attach_image(i)
        self.thread.text_message(role="user", content=m)
        response = self.thread.send()
        print(response)

# ensure the scripts run with a name = main statement
if __name__ == "__main__":
    ai = AINotes()