from django.shortcuts import render , redirect
from django.http import HttpResponseBadRequest , HttpResponseServerError , Http404
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.db.models import Q 
from django.db import transaction

### import settings 

from django.conf import settings

### rest framework imports 

from rest_framework.pagination import PageNumberPagination

### forms import 

from .forms import blogCreateForm

### import models 

from ..models import Blog

### import utils 

from .utils import BlogSerializer , BlogPaginator

### llm import 

from ..llm import get_tags


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
            with transaction.atomic():
                blog = Blog.objects.create(title=title,content=content,author=request.user)
                transaction.on_commit(lambda: get_tags(blog))
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


@login_required 
def get_personlized_blogs(request):
    try:
        user_tags = request.user.tags

        query = Q()

        if user_tags:
            for tag in user_tags:
                query |= Q(tags__contains=[tag])   

        paginator = BlogPaginator()

        feed = Blog.objects.filter(query).distinct().order_by('date_of_pub').reverse() 

        paginated_feed = paginator.paginate_queryset(queryset=feed,request=request)

        seralizer = BlogSerializer(paginated_feed,many=True)

        return paginator.get_paginated_response(seralizer.data)

        
    except Exception as error:

        print(error)

        return HttpResponseServerError('Something went wrong...')
    

@login_required 
def get_all_blogs(request):
    try:
        paginator = BlogPaginator() 

        feed = Blog.objects.all().order_by('date_of_pub').reverse()

        paginated_feed = paginator.paginate_queryset(queryset=feed,request=request)

        seralizer = BlogSerializer(paginated_feed,many=True)

        return paginator.get_paginated_response(seralizer.data)

        
    except Exception as error:

        print(error)

        return HttpResponseServerError('Something went wrong...')