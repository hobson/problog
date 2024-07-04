from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
import requests

load_dotenv()
endpoints = dict(
    openrouter=dict(
        key=os.environ.get("OPEN_ROUTER_KEY"),
        domain="openrouter.ai",
        path="api/v1",
        models_path='models'),
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
# print(f'key: {LLM_API_KEY[:3]}...{LLM_API_KEY[-2:]}')


def get_model_choices(provider='openrouter'):
    url = (
        'https:/'
        + '/' + endpoints[provider].get('domain').strip('/')
        + '/' + endpoints[provider].get('path').strip('/')
        + '/' + endpoints[provider].get('models').strip('/')
    )
    url = get_endpoint_url(provider=provider, models=True)
    resp = requests.get(url)
    data = resp.json()['data']
    return data


def get_endpoint_url(endpoint='openrouter', models=False):
    kwargs = endpoints.get(endpoint)
    url = 'https://'
    for k in ('domain path' + (models * ' models')).split():
        url += '/' + kwargs.get(k, '')
    return url

    # url = '/'.join([ for s in ])
    #     'https:/'
    #     + '/' + endpoints[provider].get('domain').strip('/')
    #     + '/' + endpoints[provider].get('path').strip('/')
    #     + '/' + endpoints[provider].get('models').strip('/')
    # )


def get_client(endpoint='openrouter', APIClass=OpenAI):  # "api.together.xyz"):
    endpoint = endpoints.get(endpoint)
    return APIClass(
        api_key=endpoint.get('key'),
        base_url=f"https://{endpoint.get('domain')}/{endpoint.get('path').strip('/')}/",
    )


def get_aclient(endpoint='openrouter', APIClass=AsyncOpenAI):  # "api.together.xyz"):
    return get_client(endpoint=endpoint, APIClass=APIClass)


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
