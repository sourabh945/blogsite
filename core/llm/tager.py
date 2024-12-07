### local import 
from django.http import HttpResponseBadRequest

from .utils import filter_tags

### models import 

from ..models import Blog 

### other modules imports 

import requests 

### celery imports 

from celery import shared_task

### import settings 

from django.conf import settings 

@shared_task(bind=True,max_retry=3,default_retry_delay=60)
def get_tags(self,id,content):
    try:
        response = requests.post(url=settings.LLM_API_URL,
                                 headers={
                                     'Authorization': f'Bearer {settings.LLM_API_KEY}',
                                     'Content-Type':'application/json',
                                     'accept':'application/json'
                                 },
                                 json={
                                     'model':settings.LLM_MODEL,
                                     'preamble':settings.LLM_PRE_PROMPT,
                                     "message":content
                                 })
        if response.status_code == 200:
            filtered_tags = filter_tags(response)
            blog = Blog.objects.get(id)
            blog.tags = filtered_tags
            blog.save()
        else:
            self.retry(countdown=60)
    except Blog.DoesNotExist as error : 
        raise error
    except Exception as error:
        return HttpResponseBadRequest('bad request sourabh')
        self.retry(countdown=60)