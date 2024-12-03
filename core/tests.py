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
        response = self.client.get('/api/posts/',HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),1)