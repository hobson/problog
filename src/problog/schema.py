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


# Schema for Conversation
class Conversation:
    def __init__(self):
        self.messages = []

    def to_dict(self):
        return {
            'messages': self.messages
        }