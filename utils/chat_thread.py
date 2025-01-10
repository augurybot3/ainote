from utils.get_client import APIClient
from utils.process_response import ProcessResponse
from utils.build_message import Message

class ChatThread:
    def __init__(self, model="gpt-4o-mini", response_format={"type":"text"}, max_t=10000, dir_path=None):
        self.messages = []
        self.counter = 0
        self.api_client = APIClient(model=model, resp_form=response_format, max_t=max_t)
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

if __name__ == "__main__":
    ct = ChatThread()