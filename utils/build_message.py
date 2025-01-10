import base64

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
    
if __name__ == "__main__":
    msg = Message()