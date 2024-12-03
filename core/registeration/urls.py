from django.urls import path

from .views import login_page , signup_page , hello_reg , logout_page

urlpatterns = [
    path('login/',login_page,name='login'),
    path('signup/',signup_page,name='signup'),
    path('hello/',hello_reg,name='hello_reg'),
    path('logout/',logout_page,name='logout'),

]