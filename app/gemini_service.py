import os
import requests
from typing import Optional

def get_gemini_api_key() -> Optional[str]:
    """Retrieve Gemini API key from environment or .env file."""
    if "GEMINI_API_KEY" in os.environ:
        return os.environ["GEMINI_API_KEY"]
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip()
        except Exception:
            pass
    return None

def generate_gemini_reasoning(prompt: str, anime_title: str) -> Optional[str]:
    """
    Optionally generate LLM-powered reasoning for an anime recommendation using Gemini.
    Falls back gracefully to None if key is absent or network is unavailable.
    """
    key = get_gemini_api_key()
    if not key:
        return None

    # Supports both v1beta and v1 standard endpoints
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    f"In 2 sentences, explain why the anime '{anime_title}' is an ideal match "
                    f"for someone asking: '{prompt}'. Keep it punchy and analytical."
                )
            }]
        }],
        "generationConfig": {
            "maxOutputTokens": 100,
            "temperature": 0.7
        }
    }

    try:
        res = requests.post(url, json=payload, timeout=3.0)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
    except Exception:
        pass
    
    return None
