import datetime

class ProcessResponse:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self._init_file()
    
    def _init_file(self):
        self.timestamp = str(datetime.datetime.now())
        self.filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    
    def log_conversation(self, messages, counter):
        # Log raw conversation data to logs.txt
        log_text = f"{counter} | {self.timestamp}\n\n{str(messages)}\n\n---\n\n"
        self._write_file("full_logs.txt", log_text)
        
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

if __name__ == "__main__":
    pr = ProcessResponse()