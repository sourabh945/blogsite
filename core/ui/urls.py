from django.urls import path 

### view import 

from .views import *

urlpatterns = [

    path('home/',home_page,name='home'),

    path('create/',create_blog_page,name='create'),

    path('blog/<str:id>/',blog_page,name='blog'),

]