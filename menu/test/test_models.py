from django.test import TestCase
from menu.models import User


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(name="Ricardo", 
                                username="ricardo",
                                password = "1234",
                                nationality="1",
                                access="1")
        
    def test_check_userdata(self):
        """Users are correctly identified"""
        user = User.objects.filter(username="ricardo").values()
        self.assertEqual(user[0]['name'], 'Ricardo')
        self.assertEqual(user[0]['username'], 'ricardo')
        self.assertEqual(user[0]['password'], '1234')