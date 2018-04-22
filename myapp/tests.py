from myapp.forms import RegisterForm, LoginForm
from django.test import TestCase, Client, RequestFactory
from django.conf import settings
# from django.urls import resolve
from django.urls import reverse
# from django.http import HttpRequest
from .views import register, login
from .models import Ads
from .forms import AdsForm
from . import broadcast as tb
import requests
import json
import os
from importlib import import_module
import mock

# Create your tests here.


class RegisterFormTest(TestCase):

    def test_valid_data(self):
        form = RegisterForm({
            'first_name': 'Test',
            'last_name': 'Account',
            'merchant_name': 'Test Merchant',
            'email': 'test@test.com',
            'password': 'test',
            'repeat_password': 'test'
        })
        self.assertTrue(form.is_valid())
        reg = form.save()
        self.assertEqual(reg.first_name, 'Test')
        self.assertEqual(reg.last_name, 'Account')
        self.assertEqual(reg.merchant_name, 'Test Merchant')
        self.assertEqual(reg.email, 'test@test.com')
        self.assertEqual(reg.password, 'test')
        self.assertEqual(reg.repeat_password, 'test')

    def test_blank_data(self):
        form = RegisterForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'merchant_name': ['This field is required.'],
            'email': ['This field is required.'],
            'password': ['This field is required.'],
            'repeat_password': ['This field is required.']
        })


class LoginFormTest(TestCase):

    def test_valid_data(self):
        form = LoginForm({
            'email': 'test@test.com',
            'password': 'test'
        })
        self.assertTrue(form.is_valid())
        log = form.save()
        self.assertEqual(log.email, 'test@test.com')
        self.assertEqual(log.password, 'test')

    def test_blank_data(self):
        form = LoginForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['This field is required.'],
            'password': ['This field is required.']
        })


class TestSession(object):

    client = Client()

    def create_session(self):
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key


class BroadcastTest(TestSession, TestCase):

    # global_mock_test = mock.Mock()
    # global_mock_test.side_effect = ConnectionError

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_broadcast_url_is_exist(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.get('/myapp/broadcast/')
        self.assertEqual(response.status_code, 200)

    def test_broadcast_page_is_completed(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.get('/myapp/broadcast/')
        # html_response = response.content.decode('utf8')

        # Checking whether all elements rendered
        self.assertTemplateUsed(response, 'myapp/template/broadcast.html')

    def test_broadcast_input_verified(self):
        Ads.objects.create(title='Testing', desc='test desc')
        url = 'https://localhost:8000/myapp/broadcast/'
        Ads.objects.create(
            title='Testing 2', desc='test desc', img=url)
        counting_all_available_message = Ads.objects.all().count()
        self.assertEqual(counting_all_available_message, 2)

    def test_form_validation_for_blank_items(self):
        form = AdsForm(data={'name': '', 'email': '', 'message': ''})
        self.assertFalse(form.is_valid())

    def get_ads(self):
        try:
            temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
            arr = json.loads(requests.get(temp).content.decode())
            arr = arr['advertisements']
        except KeyError:
            arr = []
        return arr

    def test_get_ads(self):
        result = self.get_ads() != []
        self.assertTrue(result)

    def test_not_get_ads(self):
        mock_test = mock.patch.dict(os.environ,
                                    {'JSON_API_ID': os.environ['ARR_API_ID']})
        mock_test.start()
        result = self.get_ads() == []
        self.assertTrue(result)
        mock_test.stop()

    def create_test_ads(self):
        temp = {}
        temp['title'] = 'Test'
        temp['description'] = 'Test Ad'
        temp['author'] = 'Django Test'
        temp['publish'] = '2018-04-17 17:31:08.137604+00:00'
        temp['lat'] = '0.000000000000000'
        temp['long'] = '0.000000000000000'
        temp['img'] = ''
        return temp

    def test_ads_send(self):
        arr = self.get_ads()
        temp = self.create_test_ads()
        arr.append(temp)
        self.assertEqual(tb.main(arr), True)

    @mock.patch('requests.put')
    def test_ads_not_send(self, mock):
        mock.side_effect = ConnectionError
        arr = self.get_ads()
        temp = self.create_test_ads()
        arr.append(temp)
        self.assertEqual(tb.main(arr), False)


class RegisterPageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_register_url_is_exist(self):
        response = Client().get('/myapp/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_is_completed(self):
        response = Client().get('/myapp/register/')
        self.assertTemplateUsed(response, 'myapp/template/register.html')

    def test_register_success(self):
        reg_data = {
            'first_name': 'Test',
            'last_name': 'Account',
            'merchant_name': 'Test Merchant',
            'email': 'test@test.com',
            'password': 'test',
            'repeat_password': 'test'
        }
        # self.assertRedirects(response, '/broadcast/', 302, 200)
        target = 'myapp.views.RegisterForm.is_valid'
        with mock.patch(target) as mock_register_form:
            mock_register_form.return_value = True
            request = self.factory.post(reverse("register"),
                                        data=reg_data, follow=True)
            register(request)
            mock_register_form.assert_called_once()

    def test_register_fail(self):
        reg_data = {}
        response = Client().post('/myapp/register/',
                                 data=reg_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form',
                             'first_name', ['This field is required.'])


class LoginPageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_is_exist(self):
        response = Client().get('/myapp/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_is_completed(self):
        response = Client().get('/myapp/login/')
        self.assertTemplateUsed(response, 'myapp/template/login.html')

    def test_login_success(self):
        login_data = {
            'email': 'test@test.com',
            'password': 'test'
        }
        # self.assertRedirects(response, '/broadcast/', 302, 200)
        with mock.patch('myapp.views.LoginForm.is_valid') as mock_login_form:
            mock_login_form.return_value = True
            request = self.factory.post(reverse("login"), data=login_data)
            login(request)
            mock_login_form.assert_called_once()

    def test_login_fail(self):
        login_data = {}
        response = Client().post('/myapp/login/', data=login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form',
                             'email', ['This field is required.'])


# class HeaderPageTest(TestCase):

#     def test_myapp_url_is_exist(self):
#         response = Client().get('/myapp/')
#         self.assertEqual(response.status_code, 200)

#     def test_header_url_is_exist(self):
#         response = Client().get('/myapp/header/')
#         self.assertEqual(response.status_code, 200)

#     def test_header_page_is_completed(self):
#         response = Client().get('/myapp/header/')
#         self.assertTemplateUsed(response, 'myapp/template/header.html')


# class FooterPageTest(TestCase):

#     def test_myapp_url_is_exist(self):
#         response = Client().get('/myapp/')
#         self.assertEqual(response.status_code, 200)

#     def test_footer_url_is_exist(self):
#         response = Client().get('/myapp/footer/')
#         self.assertEqual(response.status_code, 200)

#     def test_footer_page_is_completed(self):
#         response = Client().get('/myapp/footer/')
#         self.assertTemplateUsed(response, 'myapp/template/footer.html')


class LoggedinPageTest(TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_loggedin_url_is_exist(self):
        response = Client().get('/myapp/loggedin/')
        self.assertEqual(response.status_code, 302)

    def test_loggedin_success(self):
        # login_data = {
        #     'email': 'test@test.com',
        #     'password': 'test'
        # }
        # #self.assertRedirects(response, '/broadcast/', 302, 200)
        # self.assertTemplateUsed(response, 'myapp/template/broadcast.html')
        pass

    def test_loggedin_fail(self):
        pass

    # def test_loggedin_page_is_completed(self):
    #     response = Client().get('/myapp/loggedin/')
    #     self.assertTemplateUsed(response, 'myapp/template/loggedin.html')


class RegisteredPageTest(TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_registered_url_is_exist(self):
        response = Client().get('/myapp/registered/')
        self.assertEqual(response.status_code, 302)

    # def test_registered_page_is_completed(self):
    #     response = Client().get('/myapp/registered/')
    #     self.assertTemplateUsed(response, 'myapp/template/loggedin.html')


class LogoutPageTest(TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url_is_exist(self):
        response = Client().get('/myapp/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_page_is_completed(self):
        response = Client().get('/myapp/logout/')
        self.assertTemplateUsed(response, 'myapp/template/logout.html')


class InvalidLoginPageTest(TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_url_is_exist(self):
        response = Client().get('/myapp/invalid/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_page_is_completed(self):
        response = Client().get('/myapp/invalid/')
        self.assertTemplateUsed(response, 'myapp/template/invalid_login.html')


class IndexPageIndex(TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_index_url_is_exist(self):
        response = Client().get('/myapp/response/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_is_completed(self):
        response = Client().get('/myapp/response/')
        self.assertTemplateUsed(response, 'myapp/template/index.html')
