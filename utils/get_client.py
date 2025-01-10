from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


cwd = os.getcwd()

dir_path = cwd + "/logs/"
if os.path.exists(dir_path):
    pass
else:
    os.mkdir(dir_path)


class APIClient:
    def __init__(self, model="gpt-4o-mini", resp_form={"type":"text"}, t=1, max_t=10000, top_p=1, freq=0, pre_p=0):
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
    

if __name__ == "__main__":
    apic = APIClient()