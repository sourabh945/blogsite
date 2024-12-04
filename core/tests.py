from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from .models import User , Blog

class ApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='sourabh945',
            name='sourabh',
            email='sheokand.sourabh.anil@gmail.com',
            password='12345678'
        )
        response = Token.objects.get_or_create(user=self.user)
        self.token = response[0]
        self.blog = Blog.objects.create(
            title='test blog initial',
            content='this is a test blog',
            author=self.user
        )
        for i in range(10):
            Blog.objects.create(
                title=f'test blog {i}',
                content=f'this is a test blog {i}',
                author=self.user
            )

    def test_user_model(self):
        self.assertEqual(self.user.username,'sourabh945')
        self.assertEqual(self.user.name,'sourabh')
        self.assertEqual(self.user.email,'sheokand.sourabh.anil@gmail.com')


    def test_add_blog(self):
        blog = {
            'title':'test title',
            'content':'this is a test blog for test'
        }
        response = self.client.post('/api/posts/',data=blog,HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code,201)
        self.assertNotEqual(response.data['id'],self.blog.id)


    def test_get_blog_by_id(self):
        
        response = self.client.get(f'/api/posts/{self.blog.id}/',HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['title'],'test blog initial')
        self.assertEqual(response.data['content'],'this is a test blog')

    def test_get_all_blogs(self):
        page_size = 1
        count = 1
        response = self.client.get(f'/api/posts/?page_size={page_size}',HTTP_AUTHORIZATION=f'Token {self.token.key}')
        while response.data['next'] is not None:
            response = self.client.get(response.data['next'],HTTP_AUTHORIZATION=f'Token {self.token.key}')
            self.assertEqual(response.status_code,200)
            self.assertEqual(len(response.data['results']),page_size)
            count += 1
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data['results']),page_size)
        self.assertEqual(count,int(response.data['count']/page_size) + int(response.data['count']%page_size))