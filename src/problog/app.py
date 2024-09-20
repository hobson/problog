from flask import Flask, request, jsonify
import os
import json
import pandas as pd
from bson import ObjectId
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient

# Local imports
from chat.chat import chat
from schema import Conversation, Message

# ==================================================================================================>
# ======================================== GSM8K ===================================================>
# ==================================================================================================>

splits = {'train': 'main/train-00000-of-00001.parquet', 'test': 'main/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/openai/gsm8k/" + splits["train"])

df.to_csv("gsm8k.csv")

# ==================================================================================================>
# ======================================== CORS ====================================================>
# ==================================================================================================>

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# ==================================================================================================>
# ===================================== DATABASE ===================================================>
# ==================================================================================================>

load_dotenv()

DB_URI = os.getenv("DB_URI")

client = MongoClient(DB_URI)
db = client['LLM']

conversations_collection = db['conversations']
messages_collection = db['messages']

# In-memory storage for messages
message_storage = []
color_messages = []


# ==================================================================================================>
# ========================================== API ===================================================>
# ==================================================================================================>

# ====================================== / ====================================================>

@app.route("/")
def hello_world():
    try:
        collections = db.list_collection_names()
        return {"message": "Server and Database are working fine!", "collections": collections}
    except Exception as e:
        return {"message": "Error connecting to the database", "error": str(e)}, 500
    
# ====================================== /conversations (GET) ========================================>

@app.route("/conversations", methods=["GET"])
def get_conversations():
    try:
        conversations = list(conversations_collection.find())

        for conversation in conversations:
            conversation['_id'] = str(conversation['_id'])

        return jsonify({
            "conversations": conversations
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    
# ====================================== /conversations (POST) ========================================>

@app.route("/conversations", methods=["POST"])
def create_conversation():
    try:
        conversation = Conversation()
        inserted_conversation = conversations_collection.insert_one(conversation.to_dict())
        conversation_id = inserted_conversation.inserted_id
        
        return jsonify({
            "message": "Conversation created successfully",
            "conversationId": str(conversation_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ====================================== /chat ====================================================>

@app.route("/chat", methods=["POST"])
def colors():
    try:
        # Retrieve the input data
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input data"}), 400

        # Validate conversationId and messages
        conversationId = data.get('conversationId')
        if not conversationId or not ObjectId.is_valid(conversationId):
            return jsonify({"error": "Invalid or missing conversationId"}), 400
        
        messages = data.get('messages', [])
        if not messages or not isinstance(messages, list) or len(messages) == 0:
            return jsonify({"error": "No valid messages provided"}), 400

        provider = data.get('provider', 'openai')
        model = data.get('model', 'gpt-3.5-turbo')
        system_prompt = data.get('system_prompt', 'You are an AI assistant.')

        # Process user message
        user_message = messages[-1]
        role = "user"
        content = user_message.get("content", "")
        if not content:
            return jsonify({"error": "User message content is missing"}), 400
        
        colorContent = "<span>No ColorContent</span>" 
        
        # Create and store the user message
        userMessage = Message(content, role, colorContent, conversationId)
        user_message_id = messages_collection.insert_one(userMessage.to_dict()).inserted_id

        # Get AI response
        chat_response = chat(messages, provider, model, system_prompt)

        # Process AI response
        system_role = "system"
        chat_content = chat_response.get("content", "")
        chat_color_content = chat_response.get("colorContent", "")

        if not chat_content or not chat_color_content:
            return jsonify({"error": "AI response is incomplete"}), 500
        
        # Create and store the system (AI) message
        systemMessage = Message(chat_content, system_role, chat_color_content, conversationId)
        system_message_id = messages_collection.insert_one(systemMessage.to_dict()).inserted_id

        # Return the chat response to the client
        return jsonify({
            "user_message_id": str(user_message_id),
            "system_message_id": str(system_message_id),
            "chat_response": chat_response
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
# ====================================== /messages ====================================================>

@app.route("/messages", methods=["GET"])
def get_messages():
    try:
        conversationId = request.args.get('conversationId')
        if not conversationId or not ObjectId.is_valid(conversationId):
            return jsonify({"error": "Invalid or missing conversationId"}), 400
        
        # Find the conversation using the conversationId
        conversation = conversations_collection.find_one({"_id": ObjectId(conversationId)})
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
        
        # Fetch messages for the specified conversation
        messages = list(messages_collection.find({"conversationId": ObjectId(conversationId)}))
        
        # Prepare lists for messages and colorMessages
        plain_messages = []
        color_messages = []

        # Loop through the messages and create two separate structures
        for message in messages:
            plain_messages.append({
                "role": message.get("role", "user"),
                "content": message.get("content", ""),
            })
            color_messages.append({
                "role": message.get("role", "user"),
                "content": message.get("content", ""),
                "colorContent": message.get("colorContent", ""),
                "conversationId": str(message.get("conversationId", ""))  # Convert ObjectId to string
            })

        # Return the conversation and the two message structures in JSON format
        return jsonify({
            "conversation": {
                "id": str(conversation["_id"]),  # Convert ObjectId to string
                "createdAt": conversation.get("createdAt", ""),
                "title": conversation.get("title", "")
            },
            "messages": plain_messages,
            "colorMessages": color_messages
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500





# ====================================== /reset ====================================================>

@app.route("/reset", methods=["POST"])
def reset_messages():
    try:
        # Extract the conversationId from the request body
        data = request.get_json()
        conversation_id = data.get('conversationId')
        
        if not conversation_id:
            return jsonify({"error": "Conversation ID is required"}), 400
        
        # Delete all messages associated with the conversationId
        messages_collection.delete_many({"conversationId": ObjectId(conversation_id)})
        
        # Update the conversation to have empty messages
        conversations_collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"messages": []}}
        )
        
        # Fetch the updated conversation
        updated_conversation = conversations_collection.find_one({"_id": ObjectId(conversation_id)})

        return jsonify({
            "message": "Messages reset successfully",
            "conversation": updated_conversation
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====================================== debug ====================================================>

if __name__ == "__main__":
    app.run(debug=True)