### config imports 
from django.conf import settings

### utils imports 

from .utils import filters

### import other modules 

import aiohttp 
import asyncio 

async def fetch_tags(text):
    async with aiohttp.ClientSession() as session:
        try:
            tags = await session.post(settings.LLM_API_URL,
                                      headers={
                                          "Authorization": f"Bearer {settings.LLM_API}",
                                          "Content-Type": "application/json",
                                          "Accept": "application/json",
                                      },
                                      json={
                                          "model": settings.LLM_MODEL,
                                          "preamble":settings.PRE_PROMPT,
                                          "message":text
                                      })
            
            return tags.json()
        except Exception as error:
            # Log the error
            raise  error
        
def get_tags(conent:str):
    try:
        return asyncio.run(fetch_tags(conent))
    except Exception as e: 
        return []