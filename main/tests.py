import unittest

# import time

from django.test import Client, TestCase, LiveServerTestCase
from django.urls import reverse
from django.utils.timezone import now

from main.models import User
from main.forms import NewUserForm, ForgotForm, UserDataForm

from selenium import webdriver
from uuid import uuid4


class NewUserFormTestCase(TestCase):
    def helper_NewUserForm(self, username, email, password):
        # w = User.objects.create(username=username, email=email, password=password)
        data = {
            "username": username,
            "email": email,
            "password1": password,
            "password2": password,
        }
        form = NewUserForm(data=data)
        return form.is_valid()

    def test_correct_data(self):
        args = ("iib12", "b123@gmail.com", "fajneHaslo12")
        self.assertTrue(self.helper_NewUserForm(*args))

    def test_no_pass(self):
        self.assertFalse(self.helper_NewUserForm("b", "mail@wp.pl", ""))

    def test_short_pass(self):
        args = ("aa12", "email@gmail.com", "haslo")
        self.assertFalse(self.helper_NewUserForm(*args))


class ForgotFormTestCase(TestCase):
    def helper_ForgotForm(self, email):
        data = {"email": email}
        form = ForgotForm(data=data)
        return form.is_valid()

    def test_no_email(self):
        self.assertFalse(self.helper_ForgotForm(""))

    def test_wrong_email(self):
        self.assertFalse(self.helper_ForgotForm("bloooo"))

    def test_correct_email(self):
        self.assertTrue(self.helper_ForgotForm("BLO@email.com"))


class UserDataFormTestCase(TestCase):
    def helper_UserDataForm(self, username, email, name, lastname, number, address):
        data = {
            "username": username,
            "email": email,
            "name": name,
            "lastname": lastname,
            "number": number,
            "address": address,
        }
        form = UserDataForm(data=data)
        return form.is_valid()

    def test_wrong_email(self):
        args = ("bolek", "BL", "POLAK", "RANDOM", "512-332-543", "Bialystok bla")
        self.assertFalse(self.helper_UserDataForm(*args))

    def test_wrong_number(self):
        args = ("bolek", "BLO@email.com", "POLAK", "RANDOM", "512-", "Bialystok bla")
        self.assertFalse(self.helper_UserDataForm(*args))
        args = (
            "bolek",
            "BLO@email.com",
            "POLAK",
            "RANDOM",
            "12332-954",
            "Bialystok bla",
        )
        self.assertFalse(self.helper_UserDataForm(*args))

    def test_correct_data(self):
        args = (
            "bolek",
            "BLO@email.com",
            "POLAK",
            "RANDOM",
            "512-332-954",
            "Bialystok bla",
        )
        self.assertTrue(self.helper_UserDataForm(*args))
        args = (
            "bolek",
            "BLO@email.com",
            "POLAK",
            "RANDOM",
            "512332954",
            "Bialystok bla",
        )
        self.assertTrue(self.helper_UserDataForm(*args))


class registerViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def helper_register(self, username, email, password1, password2):
        self.driver.get(f"{self.live_server_url}/register/")
        self.driver.find_element_by_id("id_username").send_keys(username)
        self.driver.find_element_by_id("id_email").send_keys(email)
        self.driver.find_element_by_id("id_password1").send_keys(password1)
        self.driver.find_element_by_id("id_password2").send_keys(password2)
        self.driver.find_element_by_class_name("btn").click()

    def test_correct_register(self):
        data = {
            "username": "bolek",
            "email": "fake@gmail.com",
            "password1": "useruser123",
            "password2": "useruser123",
        }
        self.helper_register(**data)
        user = User.objects.filter(username=data["username"])
        self.assertTrue(user.exists())
        self.tearDown()

    def test_wrong_register(self):
        data = {
            "username": "bolek",
            "email": "fake@gmail.com",
            "password1": "useruser123",
            "password2": "useruser1",
        }
        self.helper_register(**data)
        user = User.objects.filter(username=data["username"])
        self.assertFalse(user.exists())
        self.tearDown()

    def test_wrong_email_register(self):
        data = {
            "username": "bolek",
            "email": "fake",
            "password1": "useruser123",
            "password2": "useruser123",
        }
        self.helper_register(**data)
        user = User.objects.filter(username=data["username"])
        self.assertFalse(user.exists())
        self.tearDown()

    def test_wrong_pass_register(self):
        data = {
            "username": "bolek",
            "email": "fake@gmail.com",
            "password1": "user",
            "password2": "user",
        }
        self.helper_register(**data)
        user = User.objects.filter(username=data["username"])
        self.assertFalse(user.exists())
        self.tearDown()

    def tearDown(self):
        self.driver.quit()


class loginViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.data = {"username": "UserOne", "password": "useruseruser"}
        self.createUser(**self.data)

    def helper_login(self, username, password):
        self.driver.get(f"{self.live_server_url}/login/")
        self.driver.find_element_by_id("id_username").send_keys(username)
        self.driver.find_element_by_id("id_password").send_keys(password)
        self.driver.find_element_by_class_name("btn").click()

    def test_correct_login(self):
        #    print(User.objects.all().get(username=data['username']).username, User.objects.all().get(username=data['username']).password)
        self.helper_login(self.data["username"], self.data["password"])
        link_text = f'Account: {self.data["username"]}'
        self.driver.find_element_by_link_text(link_text)
        self.tearDown()

    def test_wrong_pass_login(self):
        self.helper_login(username=self.data["username"], password="useaasdasd")
        #    print(self.driver)
        #    print(self.driver.current_url)
        assert self.driver.current_url == f"{self.live_server_url}/login/"
        self.tearDown()

    def test_no_user_login(self):
        self.helper_login(self.data["username"], self.data["password"])
        self.tearDown()

    def createUser(self, username, password):
        user = User.objects.create(username=username)
        user.set_password(password)
        user.activated = True
        user.save()

    def tearDown(self):
        self.driver.quit()
