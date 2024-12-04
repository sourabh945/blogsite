### config imports 
from django.conf import settings

### utils imports 

from .utils import filters

from tenacity import retry, stop_after_attempt, wait_fixed

import requests

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_tags(text):
    try:
        return requests.post(
            url=settings.LLM_API_URL,
            headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "model": settings.LLM_MODEL,
                "preamble":settings.PRE_PROMPT,
                "message":text
            },
        )
    
    except Exception as e:
        # Log the error
        raise  e


def get_tags(content: str):
    try:
        return filters.filter_tags(fetch_tags(content))
    except Exception as e: 
        return [] 
