from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
endpoints = dict(
    openrouter=dict(
        key=os.environ.get("OPEN_ROUTER_KEY"),
        domain="openrouter.ai",
        path="api/v1"),
    openai=dict(
        key=os.environ.get("OPEN_AI_KEY"),
        domain="api.openai.com",
        path="v1"),
    togetherai=dict(
        key=os.environ.get("TOGETHER_AI_KEY"),
        domain="together.ai",
        path="api/v1"),
)

LLM_API_KEY, LLM_API_FQDN, LLM_API_PATH = endpoints['openai'].values()
print(f'key: {LLM_API_KEY[:3]}...{LLM_API_KEY[-2:]}')


def get_client(key=LLM_API_KEY, domain=LLM_API_FQDN, path=LLM_API_PATH):  # "api.together.xyz"):
    return OpenAI(
        api_key=key,
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
