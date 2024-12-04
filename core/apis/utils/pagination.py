
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow users to control page size via query param
    max_page_size = 100  # Optional: limit maximum size for security
