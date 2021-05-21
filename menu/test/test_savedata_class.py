from django.test import TestCase
from menu.savedata_class import CreateUser

class test_CreateUser(TestCase):

    def setUp(self):
        self.newUser = CreateUser(name='Alvaro',username='alvaro', 
                                                password=123456,
                                                nationality='1',
                                                access='1')

    def test_variables(self):
       #test the data from createUser class is correclty return
       self.newUser.name 
       self.assertEqual(self.newUser.name , 'Alvaro')
       self.assertEqual(self.newUser.access, '1')