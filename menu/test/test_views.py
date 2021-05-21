from django.test import TestCase
from menu.models import User
from django.urls import reverse
from django.test import Client
from django.contrib.auth.hashers import make_password, check_password

class PathTest(TestCase):
    """
    This test the paths and if they can be able to enter 
    without login except the first 
    two test because they don't require authentication.
    """
    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_menuoftheday(self):
        response = self.client.get('/menuoftheday')
        self.assertEqual(response.status_code, 200) 

    def test_home(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)
    
    def test_adminform(self):
        response = self.client.get('/adminform')
        self.assertEqual(response.status_code, 302)
    
    def test_createmenu(self):
        response = self.client.get('/createmenu')
        self.assertEqual(response.status_code, 302)
    
    def test_menurequests(self):
        response = self.client.get('/menurequests')
        self.assertEqual(response.status_code, 302)
    
    def test_modifymenu(self):
        response = self.client.get('/modifymenu')
        self.assertEqual(response.status_code, 302)
    
class LoginTestCase(TestCase):
    """
    Testing the login with a given user.    
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(name='John',username = 'john',
                                            password = make_password('123456'),
                                            nationality ='1',
                                            access ='1')

    def testLogin(self):
        self.client.login(username='john', password='123456')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    
