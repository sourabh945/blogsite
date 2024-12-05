from django.shortcuts import render , HttpResponse , redirect
from django.http import HttpResponseBadRequest , HttpResponsePermanentRedirect , HttpResponseServerError , Http404
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.urls import reverse

### forms import 

from .forms import blogCreateForm

### import models 

from ..models import Blog

@login_required
def home_page(request):
    return render(request,'home/index.html',context={'csrf_token':get_token(request)})


@login_required
def create_blog_page(request):
    if request.method == 'POST':
        form = blogCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            blog = Blog.objects.create(title=title,content=content)
            if blog:
                return redirect('home')
            else:
                return HttpResponseServerError('Something went wrong...')
        else:
            return HttpResponseBadRequest('Please submit a valid form')
    return render(request,'create/index.html',context={'csrf_token':get_token(request),'form':blogCreateForm()})


@login_required
def blog_page(request,id):
    try:
        blog = Blog.objects.get(id=id)
        return render(request,'blog/index.html',context={'blog':blog})
    except Exception as error:
        print(error)
        return Http404(f'No blog is exits of id {id}')
