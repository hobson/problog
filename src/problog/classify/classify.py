def classify_user_response(bot_text, user_text):
    user_text = user_text.lower()

    # Keywords for classification
    correct_keywords = ["correct", "right", "yes", "exactly", "agreed", "true", "that's it", "fine"]
    wrong_keywords = ["wrong", "incorrect", "no", "not right", "that's not", "false", "fail"]
    
    # List of question words that commonly start a question
    question_start_keywords = [
        "what", "why", "how", "when", "where", "can", "could", "is", "are", "do", "did",
        "who", "which", "will", "would", "should", "may", "might", "shall"
    ]
    
    is_question = False
    is_correct = False
    is_wrong = False

    # Step 1: Check for question
    if user_text.endswith('?') and any(user_text.startswith(word) for word in question_start_keywords):
        is_question = True
    
    # Step 2: Check for correctness 
    if any(word in user_text for word in correct_keywords):
        is_correct = True
    
    # Step 3: Check for wrongness 
    if any(word in user_text for word in wrong_keywords):
        is_wrong = True

    # Step 4: Final classification
    if is_question:
        return "question"
    elif is_correct and not is_wrong:
        return "correct answer"
    elif is_wrong and not is_correct:
        return "wrong answer"
    elif is_correct and is_wrong:
        return "unknown answer"
    else:
        return "unknown question"