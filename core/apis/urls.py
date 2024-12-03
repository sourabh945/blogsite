from django.urls import path

##
from .views import AuthToken , get_blog_by_id , posts ,hello

urlpatterns = [
    path('api/get-token/',AuthToken.as_view(),name='get-token'),
    path('api/posts/<str:id>/',get_blog_by_id,name='get-blog-by-id'),
    path('api/posts/',posts,name='posts'),
    path('api/hello/',hello,name='api-hello'),
]