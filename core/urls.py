

urlpatterns = []

### importing the urls for the inside app registeration that for registration the users 

from .registeration.urls import urlpatterns as reg_urls

urlpatterns += reg_urls


### importing the urls for the inside app that provides all api interfaces for user 
### we not using these api into the direct applications because these needed the token which is can't stored in browser

from .apis.urls import urlpatterns as api_urls

urlpatterns += api_urls