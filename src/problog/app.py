from flask import Flask, request, jsonify, Response
import json
import os
import csv 
import re
import pandas as pd
from bson import ObjectId
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# Local imports
from chat.chat import chat, check_answer_chat
from schema import Conversation, Message, Users, File

# ==================================================================================================>
# ======================================== GSM8K ===================================================>
# ==================================================================================================>

splits = {'train': 'main/train-00000-of-00001.parquet', 'test': 'main/test-00000-of-00001.parquet'}
try:
    df = pd.read_parquet("hf://datasets/openai/gsm8k/" + splits["train"])
    df.to_csv("gsm8k.csv")
    print("Dataset saved as gsm8k.csv successfully.")
except Exception as e:
    print(f"An error occurred while fetching the dataset: {e}")

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
users = db['users']
files_collection = db['files']

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
        grouped_conversations = {}

        username = request.args.get('username')

        if not username:
            return jsonify({"error": "Username is required"}), 400

        # Fetch the user's conversations
        user_conversations = list(conversations_collection.find({"username": username}))

        # Ensure the user's conversations are added to the grouped dictionary
        grouped_conversations[username] = []
        for conversation in user_conversations:
            grouped_conversations[username].append({
                "id": str(conversation['_id']),
                "messages": conversation['messages']
            })

        # Fetch conversations from other users
        other_users_conversations = list(conversations_collection.find({"username": {"$ne": username}}))

        # Group other users' conversations
        for conversation in other_users_conversations:
            other_username = conversation['username']
            if other_username not in grouped_conversations:
                grouped_conversations[other_username] = []
            grouped_conversations[other_username].append({
                "id": str(conversation['_id']),
                "messages": conversation['messages']
            })

        # Convert the grouped dictionary to the desired response format
        response = {
            "conversations": []
        }

        # Add the current user's conversations first
        response['conversations'].append({
            "username": username,
            "conversations": grouped_conversations[username]
        })

        # Add other users' conversations
        for user, convos in grouped_conversations.items():
            if user != username:
                response['conversations'].append({
                    "username": user,
                    "conversations": convos
                })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# ====================================== /uploadFile (POST) ========================================>

def clean_math_expression(data):
    cleaned_data = re.sub(r"<<.*?>>", "", data)
    cleaned_data = cleaned_data.replace("#", "")
    return cleaned_data.strip()

ALLOWED_EXTENSIONS = {'csv'}
EXPECTED_COLUMNS = ["id", "question", "answer"]  # Original expected format
EXPECTED_COLUMNS_NO_ID = ["", "question", "answer"]  # Format with leading empty column

# Helper function to check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/uploadFile", methods=["POST"])
def uploadFile():
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        conversation_id = request.form.get('conversation_id')

        # Check if the file is selected and valid
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if file and allowed_file(file.filename):
            # Secure the filename to prevent unsafe characters
            filename = secure_filename(file.filename)
            
            # Extract file title from the filename (without extension)
            file_title = os.path.splitext(filename)[0]

            # Read the CSV file content
            file_data = []
            csv_reader = csv.reader(file.read().decode('utf-8').splitlines())
            
            # Extract the header (first row) of the CSV
            header = next(csv_reader, None)

            # Check if the header matches the expected formats
            if header == EXPECTED_COLUMNS:
                id_included = True  # The header includes "id"
            elif header == EXPECTED_COLUMNS_NO_ID:
                id_included = False  # The header doesn't include "id"
            else:
                return jsonify({
                    "error": "Invalid file format. Expected columns: 'id, question, answer' or ', question, answer'."
                }), 400

            # Process each subsequent row
            for row in csv_reader:
                if id_included and len(row) == 3:  # Full format with ID
                    question = row[1].strip()
                    answer = row[2].strip()
                    file_data.append({"question": question, "answer": clean_math_expression(answer)})
                elif not id_included and len(row) == 3:  # Format without ID (leading comma)
                    question = row[1].strip()
                    answer = row[2].strip()
                    file_data.append({"question": question, "answer": clean_math_expression(answer)})
                else:
                    return jsonify({"error": "Invalid row format in the file."}), 400

            # Get conversation ID from request
            if not conversation_id:
                return jsonify({"error": "No conversation ID provided."}), 400

            # Find conversation by ID and ensure it exists
            conversation = conversations_collection.find_one({"_id": ObjectId(conversation_id)})
            if not conversation:
                return jsonify({"error": "Conversation not found."}), 404

            # Create a new File object
            new_file = File(file_data=file_data, conversation_id=conversation_id, file_title=file_title)

            inserted_file = files_collection.insert_one(new_file.to_dict())

            # Update the conversation with the file ID
            conversations_collection.update_one(
                {"_id": ObjectId(conversation_id)},
                {"$set": {"fileId": inserted_file.inserted_id}}
            )

            return jsonify({
                "message": "File uploaded successfully", 
                "file_id": str(inserted_file.inserted_id),
                "file_title": str(file_title),
            }), 200
        else:
            return jsonify({"error": "Invalid file type. Only .csv files are allowed."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====================================== /download CONVERSATION (GET) ========================================>

@app.route("/downloadConversation", methods=["GET"])
def downloadConversation():
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
                "conversationId": str(message.get("conversationId", "")) 
            })

        # Initialize file information
        file_info = None
        file_id = conversation.get("fileId")
        
        # If there is a fileId, fetch the file information
        if file_id:
            file_data = files_collection.find_one({"_id": ObjectId(file_id)})
            if file_data:
                file_info = {
                    "fileId": str(file_data["_id"]), 
                    "fileTitle": file_data.get("file_title", ""),
                }

        response_data = {
            "conversation": {
                "id": str(conversation["_id"]), 
                "createdAt": conversation.get("createdAt", ""),
                "title": conversation.get("title", ""),
                "username": conversation.get("username"), 
            },
            "file": file_info,
            "messages": plain_messages,
            "colorMessages": color_messages
        }

        response_json = json.dumps(response_data, indent=4)
        return Response(
            response_json,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=conversation.json'}
        )

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# ====================================== /deletefile (DELETE) =========================================>

@app.route("/deleteFile", methods=["DELETE"])
def deleteFile():
    try:
        # Get the fileId from the request body (or query parameter if needed)
        file_id = request.json.get('fileId')

        if not file_id:
            return jsonify({"error": "No fileId provided"}), 400

        # Find the file by fileId
        file = files_collection.find_one({"_id": ObjectId(file_id)})

        if not file:
            return jsonify({"error": "File not found"}), 404

        # Get the associated conversation ID from the file
        conversation_id = file.get('conversation_id')

        if not conversation_id:
            return jsonify({"error": "Conversation ID not found in the file"}), 400

        # Find the conversation associated with the fileId
        conversation = conversations_collection.find_one({"fileId": ObjectId(file_id)})

        if not conversation:
            return jsonify({"error": "Conversation with the provided fileId not found"}), 404

        # Set fileId to null in the conversation
        conversations_collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"fileId": None}}
        )

        # Delete the file from files_collection
        files_collection.delete_one({"_id": ObjectId(file_id)})

        return jsonify({"message": "File and associated data deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ====================================== /conversations (POST) ========================================>

@app.route("/conversations", methods=["POST"])
def create_conversation():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input data"}), 400

        username = data.get('username')
        conversation = Conversation(username)
        inserted_conversation = conversations_collection.insert_one(conversation.to_dict())
        conversation_id = inserted_conversation.inserted_id
        
        return jsonify({
            "message": "Conversation created successfully",
            "conversationId": str(conversation_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ====================================== /search =====================================================>

@app.route("/search", methods=["POST"])
def searchQuestions():
    try:
        data = request.json
        content = data.get('content', None)  # Assuming 'content' contains the string to search for
        fileId = data.get('fileId', None)

        if not content or not fileId:
            return jsonify({"error": "Missing content or fileId in request"}), 400

        # Find the file using fileId
        file = files_collection.find_one({"_id": ObjectId(fileId)})
        if not file:
            return jsonify({"error": "File not found"}), 404

        # Use regex to search for the question in file_data
        file_data = file.get("file_data", [])

        best_match = None
        max_score = -1

        # Loop through the file_data to find the most accurate match
        for entry in file_data:
            file_question = entry.get("question", "")

            # Use regex to find matches in the question
            match = re.search(re.escape(content), file_question, re.IGNORECASE)
            if match:
                # Calculate score based on match length (adjust as needed)
                score = len(match.group(0))
                if score > max_score:
                    max_score = score
                    best_match = file_question

        if best_match:
            return jsonify({ "question": best_match })
        else:
            return jsonify({"error": "No matching question found"}), 404

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
        username = data.get('username')
        conversationId = data.get('conversationId')
        if not conversationId or not ObjectId.is_valid(conversationId):
            return jsonify({"error": "Invalid or missing conversationId"}), 400
        
        conversation = conversations_collection.find_one({"_id": ObjectId(conversationId)})
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        # Check if the conversation's username matches
        if conversation.get('username') != username:
            return jsonify({"error": "Invalid or Unauthorized"}), 400

        messages = data.get('messages', [])
        if not messages or not isinstance(messages, list) or len(messages) == 0:
            return jsonify({"error": "No valid messages provided"}), 400

        provider = data.get('provider', 'openai')
        model = data.get('model', 'gpt-3.5-turbo')
        system_prompt = data.get('system_prompt', 'You are an AI assistant.')
        fileId = data.get('fileId', None)

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

        # Conditional logic: if `fileId` is provided, use `bg_chat`, otherwise use `chat`
        if fileId and fileId != 'nofile':
            # Find the file using fileId
            file = files_collection.find_one({"_id": ObjectId(fileId)})
            if not file:
                return jsonify({"error": "File not found"}), 404

            # Use regex to search for the question in file_data
            file_data = file.get("file_data", [])
            actual_answer = None

            # Loop through the file_data to find the matching question
            for entry in file_data:
                file_question = entry.get("question", "")
                file_answer = entry.get("answer", "")

                # Use regex to match the question
                if re.search(re.escape(content), file_question, re.IGNORECASE):
                    actual_answer = file_answer
                    break

            if actual_answer is None:
                chat_response = chat(messages, provider, model, system_prompt)
            else:
                chat_response = check_answer_chat(messages, actual_answer, provider, model, system_prompt)
        else:
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

        # Initialize file information
        file_info = None
        file_id = conversation.get("fileId")
        
        # If there is a fileId, fetch the file information
        if file_id:
            file_data = files_collection.find_one({"_id": ObjectId(file_id)})
            if file_data:
                file_info = {
                    "fileId": str(file_data["_id"]), 
                    "fileTitle": file_data.get("file_title", ""),
                }

        response = {
            "conversation": {
                "id": str(conversation["_id"]), 
                "createdAt": conversation.get("createdAt", ""),
                "title": conversation.get("title", ""),
                "username": conversation.get("username"), 
            },
            "file": file_info,
            "messages": plain_messages,
            "colorMessages": color_messages
        }

        return jsonify(response), 200

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
    
# ====================================== /register user ====================================================>

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        existing_user = users.find_one({"username": username})
        
        if existing_user:
            return jsonify({"error": "Username already exists. Please choose another one."}), 409
        
        hashed_password = generate_password_hash(password)
        
        user = Users(username, hashed_password)
        result = users.insert_one(user.to_dict())
        
        return jsonify({"message": "Registration successful", "username": user.username}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ====================================== /register user ====================================================>

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Find the user by username
        result = users.find_one({"username": username})
        
        if result:
            # Verify the password
            if check_password_hash(result['password'], password):
                return jsonify({"message": "Login successful", "username": username}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "Username not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====================================== debug ====================================================>

if __name__ == "__main__":
    app.run(debug=True)