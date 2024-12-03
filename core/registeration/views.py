from django.shortcuts import render , redirect , HttpResponse
from django.http import HttpResponseBadRequest 
from django.contrib.auth import authenticate , login , decorators 
from django.middleware.csrf import get_token
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q


### model imports 

from ..models import User , ValidationIDs

### forms imports

from .forms import signup_form , login_form , verification_regen_form

### utils imports 

from .utils import send_verification_email

# Create your views here.

@decorators.login_required
def hello_reg(request):
    return HttpResponse(f'hello {request.user} ! I hope you doing well it is test page for this brach, owern: sheokand.sourabh.anil@gmail.com')


def re_gen_verification(request):
    if request.method == 'POST':
        form = verification_regen_form(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(Q(username=form.cleaned_data['email_or_username']) | Q(email=form.cleaned_data['email_or_username']))
                if user.is_verified:
                    messages.error(request=request,message='User is already verified',extra_tags='login')
                    return redirect('login')
                verification = ValidationIDs.objects.get(user=user)
                send_verification_email(user.email,reverse('verification',args=[verification.id]))
            except Exception as error:
                print(error) 
                messages.error(request=request,message='User is not register please signup first',extra_tags='signup')
                return redirect('signup')
        return HttpResponseBadRequest('Please send a valid request')
    return render(request,'verification/index.html',context={'csrf_token':get_token(request),'form':verification_regen_form()})
        

def verification(request,id:str):
    if request.method == 'GET':
        try:
            verification = ValidationIDs.objects.get(id=id)
        except Exception as error:
            print(error)
            messages.error(request=request,message='Invalid id for verification code',extra_tags='verification')
            return redirect('re_gen_verificatin')
        if verification.validate():
            messages.success(request=request,message='Your are verified please login',extra_tags='login')
            return redirect('login')
        else:
            messages.error(request=request,message='Verification code is expired. Please generate again')
            return redirect('re_gen_verification')
    

def signup_page(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],name=form.cleaned_data['name'],password=form.cleaned_data['password'])
                verification = ValidationIDs.objects.create(user=user)
                send_verification_email(user.email,reverse('verification',args=[verification.id]))
                messages.info(request=request,message='Please first check your email for verification',extra_tags='login')
                return redirect('login')
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
                    if user.is_verified:
                        login(request,user)
                        return redirect('hello_reg') ### change it to home page
                    else:
                        messages.error(request,message='User is not verified yet please check you email or regenerate the code here',extra_tags='verification')
                        return redirect('re_gen_verification')
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
    
                    