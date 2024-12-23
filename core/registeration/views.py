from django.shortcuts import render , redirect , HttpResponse
from django.http import HttpResponseBadRequest 
from django.contrib.auth import authenticate , login , decorators  , logout
from django.middleware.csrf import get_token
from django.contrib import messages
from django.db.models import Q
from django.conf import settings

## other modules import 

import json

### model imports 

from ..models import User

### forms imports

from .forms import signup_form , login_form 

# Create your views here.

HOME_PAGE = 'home'

@decorators.login_required
def hello_reg(request):
    return HttpResponse(f'hello {request.user} ! I hope you doing well it is test page for this brach, owern: sheokand.sourabh.anil@gmail.com')

def signup_page(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create(username=form.cleaned_data['username'],email=form.cleaned_data['email'],name=form.cleaned_data['name'],password=form.cleaned_data['password'])
                login(request,user)
                return redirect('tags')
            except Exception as error:
                messages.error(request=request,message='Username or email is already exists',extra_tags='login')
                return redirect('tags')
        else:
            return HttpResponseBadRequest('Please try a valid form')
    return render(request,'login/index.html',context={'csrf_token':get_token(request),'login_form':login_form(),'signup_form':signup_form()})


def login_page(request):
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            try: 
                user = User.objects.get(Q(username=form.cleaned_data['username_or_email']) | Q(email=form.cleaned_data['username_or_email']))
                password = form.cleaned_data['password']
                user = authenticate(request,username=user.username,password=password)
                if user:
                    login(request,user)
                    return redirect(HOME_PAGE) ### change it to home page
                else:
                    messages.error(request,'login credentials are wrong',extra_tags='login')
                    return redirect('login')
            except Exception as error:
                print(error)
                messages.error(request,message='User is not registered',extra_tags='signup')
                return redirect('signup')
        else:
            return HttpResponseBadRequest('Please send a valid request')
    return render(request,'login/index.html',context={'csrf_token':get_token(request),'login_form':login_form(),'signup_form':signup_form()})   
    
@decorators.login_required
def logout_page(request):
    logout(request)
    return redirect('login')

@decorators.login_required
def tags_page(request):
    if request.method == 'GET':
        tags = request.user.tags
        return render(request,'tags/index.html',context={'csrf_token':get_token(request),'tags':settings.TAG_LIST,'user_tags':tags})
    else:
        response = request.body.decode('utf-8')
        tags = json.loads(response)['tags']
        if tags:
            request.user.tags = tags
            request.user.save()
        return HttpResponse('Tags are updated successfully')