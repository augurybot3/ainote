# jupyter-chat

A basic idea that I've found useful.
Pipe into your jupyter notebook, your favorite or most convenient LLM.
Then, you can easily just start a new cell, if you like, and ask a question, or get direct code to implement.
The goal here, for this use case, requires a very simple and unobtrusive invokation, else it may defeat the purpose.

```python
from ainote import AINotes, 
ai = AINotes
response = ai.chat("here is my message to send")
```

the conversational thread can be continued or ended at will.
Simply reinvoke the `AINotes` class by assigning it to a variable to start a new thread.

```python
ai2 = AINotes
```

you can set a developer message for further instructional guidance.

```python
ai.dev_chat("this is the developer message")
response = ai.chat("this is the normal 'user' message")
```

you can also send images to chat over

```python
response = ai.image_chat("here is the text prompt", "location/path/of/your/image.jpeg")
```

The script keeps track of your messages and the model's responses in 2 log files.

The first one is a complete log, showin the total characters sent to and from.

The second log file, is a 'pretty printed' log, that shows the conversation as it would normally appear to an end user.





