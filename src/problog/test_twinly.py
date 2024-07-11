import requests
import dotenv
import os

dotenv.load_dotenv()
env = dict(os.environ)
# globals().update(dict(os.environ))
TWINLY_AI_KEY = env.get('TWINLY_AI_KEY')
WIKIPEDIA_API_KEY = env.get('WIKIPEDIA_API_KEY')
GROUNDING_TOPICS = [
    "https://en.wikipedia.org/wiki/LLM",
    "https://en.wikipedia.org/wiki/LLM_Lettering",
    "https://en.wikipedia.org/wiki/Logic_learning_machine",
    "https://en.wikipedia.org/wiki/Large_language_model",
],

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. "
    + "If you do not understand a question ask clarrifying questions or admit what you do not know."
)


def build_payload(
        prompt: str,
        api_key: str = TWINLY_AI_KEY,
        system_prompt: str = SYSTEM_PROMPT,
        **kwargs,
):
    payload = {
        "api_key": api_key,
        "model": "gpt-4o",
        "messages": [
            {
                "content": system_prompt,
                "role": "system",
            },
            {
                "content": prompt,
                # "at the same level as a 2nd grade elementary school student?",
                "role": "user",
            }
        ],
        "grounding_topics": GROUNDING_TOPICS,
        "context": "Custom context to ground the LLM's responses in"
    }
    payload.update(kwargs)
    return payload


def ask_twinly(
        prompt: str,
        base_url: str = 'https://twinlyai-j2vtca5m4q-uw.a.run.app',
        endpoint: str = 'chat_response',
        api_key=TWINLY_AI_KEY,
        **kwargs
):

    headers = {
        'User-Agent': 'Knowt (admin@totalgood.com)'
    }
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    payload = build_payload(prompt, api_key=api_key, **kwargs)
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    url = '/'.join((base_url, endpoint)) + '/'
    response = requests.post(url, headers=headers, data=payload)
    return response


def search_wikipedia(
        query: str,
        language_code: str = 'en',
        topk: int = 1,
        api_key=WIKIPEDIA_API_KEY):
    headers = {
        'User-Agent': 'Knowt (admin@totalgood.com)'
    }
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': query, 'limit': topk}
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()


if __name__ == '__main__':
    prompt = "Are LLMs capable of common sense reasoning?"
    response = ask_twinly(prompt)
    print(response)
