from django.shortcuts import render , redirect , HttpResponse
from django.http import HttpResponseBadRequest 
from django.contrib.auth import authenticate , login , decorators  , logout
from django.middleware.csrf import get_token
from django.contrib import messages
from django.db.models import Q


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
                user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],name=form.cleaned_data['name'],password=form.cleaned_data['password'])
                login(request,user)
                return redirect(HOME_PAGE)
            except Exception as error:
                print(error)
                messages.error(request=request,message='Username or email is already exists',extra_tags='login')
                return redirect('login')
        else:
            return HttpResponseBadRequest('Please try a valid form')
    return render(request,'login/index.html',context={'csrf_token':get_token(request),'login_form':login_form(),'signup_form':signup_form()})


def login_page(request):
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            try: 
                print(form.cleaned_data['username_or_email'])
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