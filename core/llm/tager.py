### local import 
from django.http import HttpResponseBadRequest

from .utils import filter_tags

### models import 

from ..models import Blog 

### other modules imports 

import requests 

### import settings 

from django.conf import settings 

def get_tags(id,content):
    try:
        response = requests.post(
            url=f'{settings.LLM_API_URL}',
            headers={
                'content-type': 'application/json',
                'authorization': f'Bearer {str(settings.LLM_API_KEY)}',
                'accept': 'application/json'
            },
            json={
                "model": f'{settings.LLM_MODEL}',
                "preamble": f'{settings.LLM_PRE_PROMPT}',
                "message": str(content)
            })
        print(response.status_code)
        if response.status_code == 200:
            filtered_tags = filter_tags(response)
            try:
                blog = Blog.objects.get(id=id)
                blog.tags = filtered_tags
                blog.save()
            except Exception as error:
                print(error)
    except Blog.DoesNotExist as error : 
        raise error
    except Exception as error:
        return HttpResponseBadRequest('bad request sourabh')