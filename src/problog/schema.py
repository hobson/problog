from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv


# Schema for Message
class Message:
    def __init__(self, content, role, colorContent, conversationId):
        self.content = content
        self.role = role
        self.colorContent = colorContent
        self.conversationId = conversationId

    def to_dict(self):
        return {
            "content": self.content,
            "role": self.role,
            "colorContent": self.colorContent,
            "conversationId": ObjectId(self.conversationId)
        }


# Schema for File
class File:
    def __init__(self, file_data, conversation_id, file_title):
        self.file_data = file_data  
        self.file_title = file_title
        self.conversation_id = conversation_id  

    def to_dict(self):
        return {
            'file_data': self.file_data,
            'file_title': self.file_title,
            'conversation_id': self.conversation_id
        }

# Schema for Conversation
class Conversation:
    def __init__(self, username):
        self.messages = []
        self.username = username
        self.fileId = None  

    def to_dict(self):
        return {
            'messages': self.messages,
            'username': self.username,
            'fileId': self.fileId
        }
    
# Schema for Conversation
class Users:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
        }