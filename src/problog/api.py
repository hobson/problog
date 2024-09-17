from chat.chat import chat

messages = [{ "role": 'user', "content": 'Tell me about San Francisco!' },]
provider = 'openai'
model = 'gpt-3.5-turbo'
system_prompt = 'You are an AI assistant.'

chat_response = chat(messages, provider, model, system_prompt)