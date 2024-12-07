from django.http import HttpResponse 

### rest api imports 

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
### models imports 

from ..models import Blog 

### utils imports

from .utils.formatter import Blog_foramtter

### import form settings 

from django.conf import settings

### import llm
 
from ..llm import get_tags


### token generator 
class AuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        response = super(AuthToken,self).post(request,*args,**kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({'username':user.username,'token':token.key})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    return Response({'message':f'Hello {request.user}'},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_blog_by_id(request,id):
    try:
        blog = Blog.objects.get(id=id)
        seralizer = Blog_foramtter(blog)
        return Response(seralizer.data,status=status.HTTP_200_OK)
    except:
        return Response({'error':f'Blog is not found ','id':id},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method=="GET":
        
        page_size = request.query_params.get('page_size',settings.DEFAULT_PAGE_SIZE)
        paginator= PageNumberPagination()
        paginator.page_size = int(page_size)
        paginator.max_page_size = settings.MAX_PAGE_SIZE

        queryset = Blog.objects.all().order_by('id')

        paginated_queryset = paginator.paginate_queryset(queryset=queryset,request=request)

        seralizer = Blog_foramtter(paginated_queryset,many=True)

        return paginator.get_paginated_response(seralizer.data)

    else:
        try:
            data = request.data
            title = data['title']
            content = data['content']
        except:
            return Response({'error':'bad request'},status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            blog = Blog.objects.create(title=title,content=content,author=request.user)
            transaction.on_commit(lambda: get_tags(blog))

        return Response({'id':blog.id},status=status.HTTP_201_CREATED)

    