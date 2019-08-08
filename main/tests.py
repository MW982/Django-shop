import unittest
#import time

from django.test import Client, TestCase, LiveServerTestCase
from django.urls import reverse
from django.utils.timezone import now

from main.models import User
from main.forms import NewUserForm, ForgotForm, UserDataForm

from selenium import webdriver
from uuid import uuid4


class NewUserFormTestCase(TestCase):
    def helper_NewUserForm(self, username, email, password):
        #w = User.objects.create(username=username, email=email, password=password) 
        data = {'username': username, 'email': email, 'password1': password, 'password2': password}
        form = NewUserForm(data=data)
        return form.is_valid()

    def test_correct_data(self):
        self.assertTrue(self.helper_NewUserForm('iib12','b123@gmail.com','fajneHaslo12'))

    def test_no_pass(self):
        self.assertFalse(self.helper_NewUserForm('b','mail@wp.pl',''))

    def test_short_pass(self):
        self.assertFalse(self.helper_NewUserForm('aa12','email@gmail.com', 'haslo'))

class ForgotFormTestCase(TestCase):
    def helper_ForgotForm(self, email):
        data = {'email': email}
        form = ForgotForm(data=data)
        return form.is_valid()

    def test_no_email(self):
        self.assertFalse(self.helper_ForgotForm(''))

    def test_wrong_email(self):
        self.assertFalse(self.helper_ForgotForm('bloooo'))
        
    def test_correct_email(self):
        self.assertTrue(self.helper_ForgotForm('BLO@email.com'))

class UserDataFormTestCase(TestCase):
    def helper_UserDataForm(self, username, email, name, lastname, number, address):
        data = {'username': username, 'email': email, 'name': name, 'lastname': lastname, 'number': number, 'address': address}
        form = UserDataForm(data=data)
        return form.is_valid()

    def test_wrong_email(self):
        self.assertFalse(self.helper_UserDataForm('bolek','BL','POLAK', 'RANDOM', '512-332-543', 'Bialystok bla'))
    
    def test_wrong_number(self):
        self.assertFalse(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '512-', 'Bialystok bla'))
        self.assertFalse(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '12332-954', 'Bialystok bla'))

    def test_correct_data(self):
        self.assertTrue(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '512-332-954', 'Bialystok bla'))
        self.assertTrue(self.helper_UserDataForm('bolek','BLO@email.com','POLAK', 'RANDOM', '512332954', 'Bialystok bla'))


class registerViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def helper_register(self, username, email, password1, password2):
        self.driver.get(f'{self.live_server_url}/register/')
        self.driver.find_element_by_id('id_username').send_keys(username)
        self.driver.find_element_by_id('id_email').send_keys(email)  
        self.driver.find_element_by_id('id_password1').send_keys(password1)
        self.driver.find_element_by_id('id_password2').send_keys(password2)
        self.driver.find_element_by_class_name('btn').click()

    def test_correct_register(self):
        data = {'username': 'bolek', 'email': 'fake@gmail.com', 'password1': 'useruser123', 'password2': 'useruser123'}
        self.helper_register(**data)
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        self.deleteUser()
        self.tearDown()

    def test_wrong_register(self):
        data = {'username': 'bolek', 'email': 'fake@gmail.com', 'password1': 'useruser123', 'password2': 'useruser1'}
        self.helper_register(**data)
        self.assertFalse(User.objects.filter(username=data['username']).exists())
        self.tearDown()

    def test_wrong_email_register(self):
        data = {'username': 'bolek', 'email': 'fake', 'password1': 'useruser123', 'password2': 'useruser123'}
        self.helper_register(**data)
        self.assertFalse(User.objects.filter(username=data['username']).exists())
        self.tearDown()

    def test_wrong_pass_register(self):
        data = {'username': 'bolek', 'email': 'fake@gmail.com', 'password1': 'user', 'password2': 'user'}
        self.helper_register(**data)
        self.assertFalse(User.objects.filter(username=data['username']).exists())
        self.tearDown()

    def deleteUser(self):
        User.objects.all().get(username='bolek').delete()

    def tearDown(self):
        self.driver.quit()

class loginViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.data = {'username': 'UserOne', 'email': 'fake@gmail.com', 'password1': 'useruseruser', 'password2': 'useruseruser'}
        self.createUser(**self.data)

    def helper_login(self, username, password):
        self.driver.get(f'{self.live_server_url}/login/')
        self.driver.find_element_by_id('id_username').send_keys(username)
        self.driver.find_element_by_id('id_password').send_keys(password)
        self.driver.find_element_by_class_name('btn').click()

    def test_correct_login(self):
    #    print(User.objects.all().get(username=data['username']).username, User.objects.all().get(username=data['username']).password)
        self.helper_login(self.data['username'], self.data['password1'])
        self.driver.find_element_by_link_text(f'Account: {self.data["username"]}')
        self.deleteUser()
        self.tearDown()

    def test_wrong_pass_login(self):
        self.helper_login(username=self.data['username'], password='useaasdasd')
    #    print(self.driver)
    #    print(self.driver.current_url)
        assert self.driver.current_url == f'{self.live_server_url}/login/'
        self.deleteUser()
        self.tearDown()

    def test_no_user_login(self):
        self.helper_login(self.data['username'], self.data['password1'])
        self.tearDown()

    def createUser(self, username, email, password1, password2):
        """
        User.objects.create doesnt work (probably beacuse it doesnt hash the passwords), 
        so in order to register the user i used selenium.
        """
        self.driver.get(f'{self.live_server_url}/register/')
        self.driver.find_element_by_id('id_username').send_keys(username)
        self.driver.find_element_by_id('id_email').send_keys(email)  
        self.driver.find_element_by_id('id_password1').send_keys(password1)
        self.driver.find_element_by_id('id_password2').send_keys(password2)
        self.driver.find_element_by_class_name('btn').click()
        user = User.objects.all().get(username=username)
        user.activated = True
        user.save()

    def deleteUser(self):
        User.objects.all().get(username='UserOne').delete()

    def tearDown(self):
        self.driver.quit()