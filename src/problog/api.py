from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
LLM_API_KEY = os.environ.get("OPEN_ROUTER_KEY")
LLM_API_FQDN, LLM_API_PATH = "api.openai.com", 'v1'
# LLM_FQDN = "api.openai.com"
# LLM_FQDN = "api.openai.com"
print(f'key: {LLM_API_KEY[:3]}...{LLM_API_KEY[-2:]}')


def get_client(domain=LLM_API_FQDN, path=LLM_API_PATH):  # "api.together.xyz"):
    return OpenAI(
        api_key=LLM_API_KEY,
        base_url=f"https://{domain}/{path.strip('/')}/",
    )


def get_aclient(domain=LLM_API_FQDN, path=LLM_API_PATH):  # "api.together.xyz"):
    return AsyncOpenAI(
        api_key=LLM_API_KEY,
        base_url=f"https://{domain}/{path.strip('/')}/",
    )


def chat():
    client = get_client()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant",
            },
            {
                "role": "user",
                "content": "Tell me about San Francisco",
            },
        ],
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_tokens=1024,
    )

    return chat_completion.choices[0].message.content
