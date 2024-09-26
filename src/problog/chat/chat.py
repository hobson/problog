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

    print("FULL TEXT RESPONSE (colored):", colored_text)
    print("---------------------------------------------------------------")
    print("FULL TEXT RESPONSE (pure):", pure_text)

    return {"colorContent": colored_text, "content": pure_text}
