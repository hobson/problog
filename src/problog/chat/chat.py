import re
import numpy as np
import markdown
from dotenv import load_dotenv
from functions.logprob import get_colors
from chat.endpoint import get_client

# ==================================================================================>
# ============================ Load environment variables ==========================>
# ==================================================================================>

load_dotenv()

# ==================================================================================>
# ============================== CHECK ANSWER ======================================>
# ==================================================================================>

def token_to_color(match):
    return "#D3D3D3" if match else "transparent"

def normalize_number(token):
    return re.sub(r'[^\d.]', '', token)

def list_of_numbers(token):
    numbers = re.findall(r'\d+(?:\.\d+)?', token)
    return numbers
            
def check_answer_chat(
    messages, 
    actual_answer,
    provider='openai', 
    model='gpt-3.5-turbo', 
    systemPrompt="You are an AI assistant", 
    maxTokens=1024,
):
    client = get_client(provider)
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": systemPrompt}, *messages],
        model=model, max_tokens=maxTokens, stream=True, logprobs=True,
    )
    
    colors = get_colors()
    colored_text = "" 
    pure_text = ""   

    norm_answer = list_of_numbers(actual_answer)
    for chunk in response:
        choice = chunk.choices[0]
        content = choice.delta.content
        log_probs = choice.logprobs
        if content and log_probs:
            pure_text += content 

            log_prob = log_probs.content[0].logprob
            linear_prob = np.round(np.exp(log_prob) * 100, 2)
            color_index = int(linear_prob // (100 / (len(colors) - 1)))
            color = colors[color_index]
            norm_token = normalize_number(content)
            pattern = r"\b" + re.escape(content.strip()) + r"\b"
            match = re.search(pattern, actual_answer, re.IGNORECASE) or (norm_token and norm_token in norm_answer)

            html_content = f'<span style="color:{color}; background-color:{token_to_color(bool(match))};">{content}</span>'

            colored_text += html_content

    return {"colorContent": colored_text, "content": pure_text}
    
# ==================================================================================>
# ========================================= CHAT ===================================>
# ==================================================================================>

def chat(
        messages, 
        provider='openai', 
        model='gpt-3.5-turbo', 
        systemPrompt="You are an AI assistant", 
        maxTokens=1024
    ):
    client = get_client(provider)
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": systemPrompt}, *messages],
        model=model, max_tokens=maxTokens, stream=True, logprobs=True,
    )
    
    colors = get_colors()
    colored_text = "" 
    pure_text = ""

    for chunk in response:
        choice = chunk.choices[0]
        content = choice.delta.content
        log_probs = choice.logprobs
        if content and log_probs:
            pure_text += content 

            log_prob = log_probs.content[0].logprob
            linear_prob = np.round(np.exp(log_prob) * 100, 2)
            color_index = int(linear_prob // (100 / (len(colors) - 1)))
            color = colors[color_index]

            html_content = f'<span style="color:{color};">{content}</span>'

            colored_text += html_content
    
    return {"colorContent": colored_text, "content": pure_text}
