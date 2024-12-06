from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from .models import User , Blog

from .llm import get_tags

import json

from django.conf import settings

from random import choices , choice

from django.contrib.auth import login

tl = settings.TAG_LIST

class ApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='sourabh945',
            name='sourabh',
            email='sheokand.sourabh.anil@gmail.com',
            password='12345678',
            tags=choices(tl,k=5)
        )
        response = Token.objects.get_or_create(user=self.user)
        self.token = response[0]
        self.blog = Blog.objects.create(
            title='test blog initial',
            content='this is a test blog',
            author=self.user,
            tags=choices(tl,k=5)
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
        for i in range(10):
            Blog.objects.create(
                title=f'test blog {i}',
                content=f'this is a test blog {i}',
                author=self.user,
                tags=choices(tl,k=5)
            )
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


class LLM_test(TestCase):

    def setUp(self):
        self.test_blog = """Introduction to Quantum Computing
                            Quantum computing is a revolutionary field of science and technology that leverages the principles of quantum mechanics to perform computations. Unlike classical computers, which process data in binary (0s and 1s), quantum computers use qubits—quantum bits that can exist in multiple states simultaneously due to superposition. This capability allows quantum computers to solve complex problems much faster than traditional computers.

                            How Quantum Computing Works
                            Qubits and Superposition: Qubits can represent both 0 and 1 simultaneously, thanks to the quantum property of superposition. This allows quantum computers to process vast amounts of data in parallel.
                            Entanglement: Quantum entanglement enables qubits to be interconnected in such a way that the state of one qubit can instantly influence another, even if they are far apart. This boosts computational power exponentially.
                            Quantum Gates: Just like classical computers use logic gates, quantum computers use quantum gates to manipulate qubit states, enabling complex operations.
                            Applications of Quantum Computing
                            Cryptography: Quantum computing poses a threat to traditional cryptographic systems like RSA, as it can factor large numbers efficiently. Post-quantum cryptography is being developed to counteract this threat.
                            Drug Discovery: Simulating molecular interactions is exponentially faster, enabling breakthroughs in pharmaceutical research.
                            Optimization Problems: Quantum algorithms can solve optimization problems in logistics, finance, and supply chain management faster than classical counterparts.
                            Challenges in Quantum Computing
                            Error Rates: Qubits are highly sensitive to environmental disturbances, causing frequent errors. Error correction is a major area of research.
                            Scalability: Building large-scale quantum computers with many stable qubits is a significant engineering challenge.
                            Cost and Accessibility: Quantum computers are expensive to develop and maintain, limiting access to large institutions and research labs.
                            Future Prospects
                            The future of quantum computing looks promising, with tech giants like IBM, Google, and Microsoft investing heavily in quantum research. As technology advances, we may see quantum computing becoming a part of everyday applications, revolutionizing industries like healthcare, finance, and artificial intelligence.
                            """
        self.user = User.objects.create(
            username='sourabh9',
            name='sourabh',
            email='sheokand.sourabh@gmail.com',
            password='12345678'
        )
        response = Token.objects.get_or_create(user=self.user)
        self.token = response[0]
        self.blog = Blog.objects.create(
            title='test blog initial',
            content='this is a test blog',
            author=self.user
        )

    def test_direct_llm(self):
        tags = get_tags(self.test_blog)


class UI_COMPONENTS_TEST(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(
            name='sourabh',
            username='sourabh945',
            email='sheokand.sourabh@gmail.com',
            password='12345678',
            tags = choices(tl,k=5)
        )
        self.user2 = User.objects.create(
            name='sourabh2',
            username='sourabh9452',
            email='sheokand.sourabh2@gmail.com',
            password='12345678',
            tags = choices(tl,k=5)
        )
        self.blogs = [] 
        for i in range(0,20):
            self.blogs.append(Blog.objects.create(
                title=f'title for text {i}',
                content=f'content for text {i}',
                author=choice([self.user1,self.user2]),
                tags=choices(tl,k=5)
            ))

    def test_feeds(self):
        response = self.client.login(username=self.user1.username,password='12345678')
        self.assertEqual(response,True)
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code,200)
        def findintersection(tags):
            return [i for i in tags if i in self.user1.tags]
        data = json.loads(response.content.decode('utf-8'))
        for i in data['results']:
            self.assertNotEqual(len(findintersection(i['tags'])),0)

    def test_home_page(self):
        self.client.login(username=self.user1.username,password='12345678')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)