from flask import Flask, request
import json
from chat.chat import chat

import pandas as pd

splits = {'train': 'main/train-00000-of-00001.parquet', 'test': 'main/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/openai/gsm8k/" + splits["train"])

df.to_csv("gsm8k.csv")

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# In-memory storage for messages
message_storage = []
color_messages = []

@app.route("/")
def hello_world():
    return {"message": "Server is working fine!"}

@app.route("/chat", methods=["POST"])
def colors():
    data = request.json
    messages = data.get('messages', [])
    provider = data.get('provider', 'openai')
    model = data.get('model', 'gpt-3.5-turbo')
    system_prompt = data.get('system_prompt', 'You are an AI assistant.')

    message_storage.append(messages[-1])
    color_messages.append(messages[-1])
    
    chat_response = chat(messages, provider, model, system_prompt)
    content = {'role': 'system', 'content': chat_response["content"]}
    colorContent = {'role': 'system', 'content': chat_response["colorContent"]}
    message_storage.append(content)
    color_messages.append(colorContent)

    return chat_response

@app.route("/messages", methods=["GET"])
def get_messages():
    print({"colorMessages": color_messages, "messages": message_storage })
    return {"colorMessages": color_messages, "messages": message_storage }

@app.route("/reset", methods=["POST"])
def reset_messages():
    message_storage.clear()
    color_messages.clear()
    return {"message": "Messages reset successfully"}

if __name__ == "__main__":
    app.run(debug=True)



# {'colorMessages': 
#  [
#      {'role': 'user', 'content': 'Hello'}, 
#      'Hello! How can I assist you today?'], 
#      'messages': [{'role': 'user', 'content': 'Hello'}, '<span style="color:#482575;">Hello</span><span style="color:#440154;">!</span><span style="color:#440154;"> How</span><span style="color:#482575;"> can</span><span style="color:#440154;"> I</span><span style="color:#482575;"> assist</span><span style="color:#440154;"> you</span><span style="color:#440154;"> today</span><span style="color:#440154;">?</span>']}
