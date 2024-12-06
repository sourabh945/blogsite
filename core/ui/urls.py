from django.urls import path 

### view import 

from .views import *

urlpatterns = [

    path('home/',home_page,name='home'),

    path('create/',create_blog_page,name='create'),

    path('blog/<str:id>/',blog_page,name='blog'),

    path('feed/',get_personlized_blogs,name='feed'),

    path('feed_all/',get_all_blogs,name='all_feed')

]