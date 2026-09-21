import os
import json
import time
import requests

def call_live_llm(prompt, system_instruction="", provider="gemini", api_key="", model=None):
    """
    Calls external LLM provider if configured. Returns response text or None on failure.
    """
    if not api_key:
        return None
        
    try:
        if provider == "gemini":
            # Gemini REST API
            model_name = model or "gemini-1.5-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": f"{system_instruction}\n\n{prompt}"}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 2048,
                    "responseMimeType": "application/json"
                }
            }
            resp = requests.post(url, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Gemini API Error {resp.status_code}: {resp.text}")
                return None
                
        elif provider == "openai":
            # OpenAI REST API
            model_name = model or "gpt-4o-mini"
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"}
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"OpenAI API Error {resp.status_code}: {resp.text}")
                return None

        elif provider == "anthropic":
            # Anthropic REST API
            model_name = model or "claude-3-haiku-20240307"
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "system": system_instruction,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2048,
                "temperature": 0.2
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                return data["content"][0]["text"]
            else:
                print(f"Anthropic API Error {resp.status_code}: {resp.text}")
                return None
                
    except Exception as e:
        print(f"Exception calling live LLM ({provider}): {e}")
        return None
        
    return None
