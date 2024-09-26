import os
import numpy as np
import tastymap as tm
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI

# ==================================================================================>
# ============================ API Endpoints Configuration =========================>
# ==================================================================================>

endpoints = {
    'openrouter': {
        'key': os.getenv("OPEN_ROUTER_KEY"),
        'domain': "openrouter.ai",
        'path': "api/v1",
        'models': ['openai/gpt-3.5-turbo'],
    },
    'openai': {
        'key': os.getenv("OPEN_AI_KEY"),
        'domain': "api.openai.com",
        'path': "v1",
        'models': ['gpt-3.5-turbo'],
    },
    'togetherai': {
        'key': os.getenv("TOGETHER_AI_KEY"),
        'domain': "together.ai",
        'path': "api/v1"
    },
}

# ==================================================================================>
# ================================ GET Endpoint URL ================================>
# ==================================================================================>

def get_endpoint_url(provider='openai', models=False):
    """Constructs the endpoint URL for the given provider."""
    provider_info = endpoints.get(provider, {})
    domain = provider_info.get('domain', '')
    path = provider_info.get('path', '')
    models_segment = 'models' if models else ''
    url = f'https://{domain}/{path}/{models_segment}'
    print('URL:', url)
    return url

# ==================================================================================>
# =================================== GET Client ===================================>
# ==================================================================================>

def get_client(provider='openai', APIClass=OpenAI):
    """Initializes and returns a client for the specified provider."""
    endpoint_info = endpoints.get(provider, {})
    api_key = endpoint_info.get('key', '')
    base_url = f"https://{endpoint_info.get('domain', '')}/{endpoint_info.get('path', '')}/"
    return APIClass(api_key=api_key, base_url=base_url)

# ==================================================================================>
# =================================== GET AClient ==================================>
# ==================================================================================>

def get_aclient(provider='openai', APIClass=AsyncOpenAI):
    """Gets an asynchronous client for the specified provider."""
    client = get_client(provider, APIClass)
    print('Client:', client)
    return client
