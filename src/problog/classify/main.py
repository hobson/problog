from classify.classify import classify_user_response

def classify_conversations(conversations):
    classified_conversations = []

    for conversation in conversations:
        conversation_id = conversation["conversationId"]
        message_pairs = conversation["messages"]
        username = conversation.get("username", "Unknown")

        for bot_message, user_message in message_pairs:
            classification = classify_user_response(bot_message, user_message)
            classified_conversations.append([conversation_id, username, bot_message, user_message, classification])

    return classified_conversations
