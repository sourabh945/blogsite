import sys

### background task imports 

from django_rq import job ,get_queue , enqueue


from django.db import transaction 

### config imports 
from django.conf import settings

### utils imports 

from .utils import filters

## models imports 
from ..models import Blog

### import other modules 

import requests
from tenacity import retry, stop_after_attempt , wait_fixed

@retry(stop=stop_after_attempt(3),wait=wait_fixed(1))
def fetch_tags(text):
        try:
            url = settings.LLM_API_URL
            return requests.post(url,
                                headers={
                                    "Authorization": f"bearer {settings.LLM_API_KEY}",
                                    "content-Type": "application/json",
                                    "accept": "application/json",
                                },
                                json={
                                    "model": settings.LLM_MODEL,
                                    "preamble":str(settings.LLM_PRE_PROMPT),
                                    "message":text
                                })
        except Exception as error:
            print(error)
            raise  error
        

@job  
def apply_tags(id,content):
    tags = fetch_tags(content)
    tags = filters.filter_tags(tags)
    with transaction.atomic() : 
        try:
            blog = Blog.objects.get(id=id)
            blog.tags = tags 
            blog.save()
        except Blog.DoesNotExist:
            print('error')
            raise Blog.DoesNotExist('at apply tags')
        

def get_tags(blog):
    id = blog.id
    content = blog.content
    queue = get_queue('default')
    queue.enqueue(apply_tags,id,content)