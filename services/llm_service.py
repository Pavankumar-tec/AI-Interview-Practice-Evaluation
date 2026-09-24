"""Provider adapters. No credentials or provider error bodies are logged."""
import requests


def call_live_llm(prompt, system_instruction='', provider='openai', api_key='', model=None):
    if not api_key or not model:
        return None
    try:
        if provider == 'openai':
            response = requests.post('https://api.openai.com/v1/chat/completions',
                headers={'Authorization': 'Bearer ' + api_key}, json={
                    'model': model, 'messages': [{'role': 'system', 'content': system_instruction}, {'role': 'user', 'content': prompt}],
                    'temperature': 0.2, 'response_format': {'type': 'json_object'}}, timeout=60)
            response.raise_for_status()
            data = response.json()
            return {'text': data['choices'][0]['message']['content'], 'model': data.get('model', model), 'usage': data.get('usage')}
        if provider == 'gemini':
            response = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                headers={'x-goog-api-key': api_key}, json={
                    'contents': [{'role': 'user', 'parts': [{'text': system_instruction + '\n' + prompt}]}],
                    'generationConfig': {'temperature': 0.2, 'responseMimeType': 'application/json'}}, timeout=60)
            response.raise_for_status()
            data = response.json()
            return {'text': data['candidates'][0]['content']['parts'][0]['text'], 'model': data.get('modelVersion', model), 'usage': data.get('usageMetadata')}
        if provider == 'anthropic':
            response = requests.post('https://api.anthropic.com/v1/messages',
                headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01'}, json={
                    'model': model, 'system': system_instruction, 'messages': [{'role': 'user', 'content': prompt}],
                    'temperature': 0.2, 'max_tokens': 2048}, timeout=60)
            response.raise_for_status()
            data = response.json()
            return {'text': ''.join(block.get('text', '') for block in data['content']), 'model': data.get('model', model), 'usage': data.get('usage')}
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
    return None
