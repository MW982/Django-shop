from django.test import TestCase
from main.models import User

from .forms import NewUserForm, ForgotForm, UserDataForm
from django.utils.timezone import now
from uuid import uuid4

class FormsTestCase(TestCase):
    def helper_NewUserForm(self, username, email, password):
        #w = User.objects.create(username=username, email=email, password=password) 
        data = {'username': username, 'email': email, 'password1': password, 'password2': password}
        form = NewUserForm(data=data)
        return form.is_valid()

    def test_NewUserForm(self):
        self.assertTrue(self.helper_NewUserForm('iib12','b123@gmail.com','fajneHaslo12'))
        self.assertFalse(self.helper_NewUserForm('b','mail@wp.pl',''))
        self.assertFalse(self.helper_NewUserForm('aa12','email@gmail.com', 'haslo'))


    def helper_ForgotForm(self, email):
        data = {'email': email}
        form = ForgotForm(data=data)
        return form.is_valid()

    def test_ForgotForm(self):
        self.assertFalse(self.helper_ForgotForm(''))
        self.assertFalse(self.helper_ForgotForm('bloooo'))
        self.assertTrue(self.helper_ForgotForm('BLO@email.com'))


    def helper_UserDataForm(self, username, email, name, lastname, number, address):
        data = {'username': username, 'email': email, 'name': name, 'lastname': lastname, 'number': number, 'address': address}
        form = UserDataForm(data=data)
        return form.is_valid()

    def test_UserDataForm(self):
        self.assertFalse(self.helper_UserDataForm('bolek','BL','POLAK', 'RANDOM', '512-332-543', 'Bialystok bla'))
        self.assertFalse(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '512-', 'Bialystok bla'))
        self.assertFalse(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '12332-954', 'Bialystok bla'))

        self.assertTrue(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '512-332-954', 'Bialystok bla'))
        self.assertTrue(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '512332954', 'Bialystok bla'))


# LATER
class ViewsTestCase(TestCase):
    def helper_resetPass(self, username='example', linkID=uuid4, password='bolek123', resetTime=now):
        data = {'username':username, 'linkID': linkID, 'password': password, 'resetTime': resetTime}
        u = User(data)
        return u

    def test_resetPass(self):
        print('\n\n\n')
        print(self.helper_resetPass())
        return True
