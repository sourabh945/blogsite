

urlpatterns = []

### importing the urls for the inside app registeration that for registration the users 

from .registeration.urls import urlpatterns as reg_urls

urlpatterns += reg_urls