

urlpatterns = []

### importing the urls for the inside app registeration that for registration the users 

from .registeration.urls import urlpatterns as reg_urls

urlpatterns += reg_urls


### importing the urls for the inside app that provides all api interfaces for user 
### we not using these api into the direct applications because these needed the token which is can't stored in browser

from .apis.urls import urlpatterns as api_urls

urlpatterns += api_urls

##3 importing the urls from the ui page that hold the home page and all main ui elements 

from .ui.urls import urlpatterns as ui_urls


urlpatterns += ui_urls


### adding index page url

from django.urls import path , include
from .views import index

urlpatterns += [
    path('',index,name='index'),
]

### implimenting django-rq

urlpatterns += [
    path('django-rq/',include('django_rq.urls'))
]