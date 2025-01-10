import os
from utils.chat_thread import ChatThread

class AINote:
    def __init__(self):
        self.model, self.max_t, self.dir_path = self.settings()
        self.thread = ChatThread(model=self.model, max_t=self.max_t, dir_path=self.dir_path)

    def settings(self, model="gpt-4o-mini", max_t=10000, dir_path=None):

        model = model
        max_t = max_t
        if dir_path:
            dir_path = dir_path
        else : dir_path = os.getcwd() + "/logs/"

        return model, max_t, dir_path
    
# when using a `set` function, the messages are appended to the current conversational thread and will appear in the logs.
# the 'developer' message is OpenAI's updated syntax for what was previously known as and is commonly referred to as the 'system' message.

    def set_developer(self,m):

        self.thread.text_message(role="developer", content=m)

    def set_user(self,m):

        self.thread.text_message(role="user", content=m)

    def set_assist(self,m):

        self.thread.text_message(role="assistant", content=m)

    def set_image(self, i, m=""):

        """i is a local path to an image"""

        self.thread.attach_image(i)
        self.thread.text_message(role="user", content=m) # adding a message is optional

# to send the current conversational thread without adding any more messages, use the following function

    def send(self, print_response=True):

        """this will send the full conversational thread, as is, to the provider."""

        response = self.thread.send()

        """`response` represents a successful response from the provider. It is automatically appended to the conversational thread as an assistant message, whether it's returned or not"""

        if print_response:
            print(response)
        return response

# use the following methods to quickly and easily send and receive responses from the AI/LLM provider.

    def chat(self,m, print_response=True):

        """Most common method: 
        this will send the full conversational thread along with your included user message to the model provider.
        It will append the message and and the successful server response (as an assistant message) to both the current conversation and recorded logs"""

        self.thread.text_message(role="user", content=m)
        response = self.thread.send()

        if print_response:
            print(response)
        return response
    
    def image_chat(self, i, m, print_response=True):

        """i is a local path to an image or an image url address
        The image_chat method will send the full conversational thread along with your image and any included message.
        It will append the image, message and and the successful server response (as an assistant message) to both the current conversation and recorded logs"""

        self.thread.attach_image(i)
        self.thread.text_message(role="user", content=m) # adding a message is optional
        response = self.thread.send()
        
        if print_response:
            print(response)

        return response


if __name__ == "__main__":
    ai = AINote()
