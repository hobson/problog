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
        models=['openai/gpt-3.5-turbo'],
        # models_path='models'
    ),
    openai=dict(
        key=os.environ.get("OPEN_AI_KEY"),
        domain="api.openai.com",
        path="v1",
        models=['gpt-3.5-turbo'],
    ),
    togetherai=dict(
        key=os.environ.get("TOGETHER_AI_KEY"),
        domain="together.ai",
        path="api/v1"
    ),
)

LLM_API_KEY, LLM_API_FQDN, LLM_API_PATH = endpoints['openai'].values()
# print(f'key: {LLM_API_KEY[:3]}...{LLM_API_KEY[-2:]}')


def get_model_choices(provider=None):
    provider = provider or next(endpoints.keys())
    url = (
        'https:/'
        + '/' + endpoints.get(provider, {}).get('domain').strip('/')
        + '/' + endpoints.get(provider, {}).get('path').strip('/')
        + '/' + endpoints.get(provider, {}).get('models').strip('/')
    )
    url = get_endpoint_url(provider=provider, models=True)
    resp = requests.get(url)
    data = resp.json()['data']
    return data


def get_endpoint_url(provider=None, models=False):
    provider = provider or next(endpoints.keys())
    kwargs = endpoints.get(provider)
    url = 'https://'
    for k in ('domain path' + (models * ' models')).split():
        url += '/' + kwargs.get(k, '')
    print('url:', url)
    return url

    # url = '/'.join([ for s in ])
    #     'https:/'
    #     + '/' + endpoints[provider].get('domain').strip('/')
    #     + '/' + endpoints[provider].get('path').strip('/')
    #     + '/' + endpoints[provider].get('models').strip('/')
    # )


def get_client(provider='openai', APIClass=OpenAI):  # "api.together.xyz"):
    endpoint = endpoints.get(provider)
    return APIClass(
        api_key=endpoint.get('key'),
        base_url='https://' + endpoint.get('domain').strip(' / ') + ' / ' + endpoint.get('path').strip(' / ') + ' /'
    )


def get_aclient(provider='openai', APIClass=AsyncOpenAI):  # "api.together.xyz"):
    provider = provider or next(endpoints.keys())
    client = get_client(provider, APIClass=APIClass)
    print('get_aclient:', client)
    return client


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
