from django.urls import path

from .views import login_page , signup_page , verification , re_gen_verification , hello_reg

urlpatterns = [
    path('login/',login_page,name='login'),
    path('signup/',signup_page,name='signup'),
    path('verification/<uuid:id>',verification,name='verification'),
    path('re-gen-verification/',re_gen_verification,name='re_gen_verification'),
    path('hello/',hello_reg,name='hello_reg')
]