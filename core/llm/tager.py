

from django.conf import settings
import textrazor
from tenacity import retry, stop_after_attempt, wait_fixed

textrazor.api_key = settings.TEXTRAZOR_API_KEY
client = textrazor.TextRazor(extractors=["topics"])

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_tags(text):
    try:
        response = client.analyze(text)
        tags = [topic for topic in response.topics()][:10]  # Limit to 10 tags
        return tags
    except textrazor.TextRazorAnalysisException as e:  # Handle specific API errors
        raise  e
    except Exception as e:
        # Log the error
        raise  e


def get_tags(content: str):
    try:
        return fetch_tags(content)
    except Exception as e: 
        return [] 
