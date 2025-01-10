import os
from utils.chat_thread import ChatThread

class AINote:
    def __init__(self):
        cwd = os.getcwd()
        dir_path = cwd + "/logs/"
        self.settings = ChatThread(model="gpt-4o-mini", max_t=10000, dir_path=dir_path)


# use the following `set` methods to include a developer message (previously known as a `system` message) and or build a RAG-like prompt.
# when using a `set` function, the messages are added to the conversational thread and will appear in the logs.

    def set_developer(self,m):

        self.settings.text_message(role="developer", content=m)

    def set_user(self,m):

        self.settings.text_message(role="user", content=m)

    def set_assist(self,m):

        self.settings.text_message(role="assistant", content=m)

    def set_image(self, i, m=""):

        """i is a local path to an image"""

        self.settings.attach_image(i)
        self.settings.text_message(role="user", content=m) # adding a message is optional

# to send the current conversational thread without adding any more messages, use the following function

    def send(self, print_response=True):

        """this will send the full conversational thread"""

        response = self.settings.send()

        """`response` is automatically added to the conversational thread as an assistant message, whether it's returned or not"""

        if print_response:
            print(response)
        return (response)

# use the following methods to send and receive responses the normal, conversational way

    def chat(self,m, print_response=True):

        """Most common method: 
        this will send the full conversational thread along with your included user message.
        It will add both your message and the response to both the current conversation and recorded logs"""

        self.settings.text_message(role="user", content=m)
        response = self.settings.send()
        if print_response:
            print(response)
        return (response)

    def image_chat(self, i, m, print_response=True):

        """i is a local path to an image or an image url address"""

        """this will send the full conversational thread along with your included user message.
        It will add both your message and the response to both the current conversation and recorded logs"""

        self.settings.attach_image(i)
        self.settings.text_message(role="user", content=m) # adding a message is optional
        response = self.settings.send()
        if print_response:
            print(response)
        return (response)


if __name__ == "__main__":
    ai = AINote()