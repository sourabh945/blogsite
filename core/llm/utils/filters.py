
from django.conf import settings

def filter_tags(response):

    tags = [i.strip() for i in response.json()['text'].split(',') if i.strip() in settings.TAG_LIST]

    return tags
