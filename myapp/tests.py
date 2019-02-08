from myapp.forms import RegisterForm, LoginForm
from django.test import TestCase, Client, RequestFactory
from django.conf import settings
from django.urls import reverse
from .views import register, login, get_user_data
from .models import Ads
from .forms import AdsForm
# from . import broadcast as tb
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

    def create_test_ads(self, img=''):
        temp = {}
        temp['title'] = 'Test'
        temp['desc'] = 'Test Ad'
        temp['latitude'] = '0.000000000000000'
        temp['longitude'] = '0.000000000000000'
        temp['fileupload'] = img
        temp['tag'] = '1'
        return temp

    def test_ads_send_without_img(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        # arr = self.get_ads()
        # arr.append(temp)
        request = self.client.post('/myapp/broadcast/', data=self.create_test_ads())
        self.assertEqual(request.status_code, 302)

    def test_ads_send_with_img(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        img = open('static/image/coba.jpeg', 'rb')
        # arr = self.get_ads()
        # arr.append(temp)
        request = self.client.post('/myapp/broadcast/', data=self.create_test_ads(img))
        self.assertEqual(request.status_code, 302)

    @mock.patch('requests.put')
    def test_ads_not_send(self, mock):
        mock.side_effect = ConnectionError
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        # arr = self.get_ads()
        # arr.append(temp)
        request = self.client.post('/myapp/broadcast/', data=self.create_test_ads())
        self.assertEqual(request.status_code, 302)

    def test_send_ads_after_reset_database(self):
        self.clear_arr()
        mock_test = mock.patch.dict(os.environ, {'JSON_API_ID': '89axb'})
        mock_test.start()
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        # arr = self.get_ads()
        # arr.append(temp)
        request = self.client.post('/myapp/broadcast/', data=self.create_test_ads())
        mock_test.stop()
        self.assertEqual(request.status_code, 302)

    def test_not_logged_in(self):
        self.create_session()
        session = self.client.session
        session['email'] = ''
        session.save()
        request = self.client.get('/myapp/broadcast/')
        self.assertEqual(request.status_code, 302)

    @mock.patch('imgurpython.ImgurClient.upload_from_path')
    def test_ads_cannot_upload_image(self, mock):
        mock.side_effect = ConnectionError
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        img = open('static/image/coba.jpeg', 'rb')
        # arr = self.get_ads()
        # arr.append(temp)
        request = self.client.post('/myapp/broadcast/', data=self.create_test_ads(img))
        self.assertEqual(request.status_code, 302)

    def clear_arr(self):
        temp = json.dumps({})
        url = 'https://api.myjson.com/bins/89axb'
        headers = {'Content-type': 'application/json'}
        return requests.put(url, data=temp, headers=headers)


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


class LoggedinPageTest(TestSession, TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_loggedin_url_is_exist(self):
        response = self.client.get('/myapp/loggedin/')
        self.assertEqual(response.status_code, 302)

    def test_loggedin_success(self):
        login_data = {
            'email': 'test@test.com',
            'password': 'test'
        }
        request = self.client.post('/myapp/loggedin/', data=login_data, follow=True)
        self.assertRedirects(request, '/myapp/broadcast/')

    def test_loggedin_fail(self):
        login_data = {
            'email': '',
            'password': ''
        }
        request = self.client.post('/myapp/loggedin/', data=login_data, follow=True)
        self.assertRedirects(request, '/login/')

    def test_loggedin_fail_password_not_equal(self):
        login_data = {
            'email': 'test@test.com',
            'password': 'testt'
        }
        request = self.client.post('/myapp/loggedin/', data=login_data, follow=True)
        self.assertRedirects(request, '/login/')

    @mock.patch('requests.get')
    def test_loggedin_key_error(self, mock):
        mock.side_effect = KeyError
        login_data = {
            'email': 'test@test.com',
            'password': 'test'
        }
        request = self.client.post('/myapp/loggedin/', data=login_data, follow=True)
        self.assertRedirects(request, '/register/')


class RegisteredPageTest(TestSession, TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_registered_url_is_exist(self):
        response = Client().get('/myapp/registered/')
        self.assertEqual(response.status_code, 302)

    def test_registered_success(self):
        register_data = {
            'first_name': 'Test',
            'last_name': 'Account',
            'merchant_name': 'Test Merchant',
            'email': 'test@test.com',
            'password': 'test',
            'repeat_password': 'test'
        }
        request = self.client.post('/myapp/registered/', data=register_data, follow=True)
        self.assertRedirects(request, '/myapp/broadcast/')

    def test_registered_fail(self):
        register_data = {
            'first_name': 'Test',
            'last_name': 'Account',
            'merchant_name': 'Test Merchant',
            'email': 'test@test.com',
            'password': 'test',
            'repeat_password': 'testt'
        }
        request = self.client.post('/myapp/registered/', data=register_data, follow=True)
        self.assertRedirects(request, '/register/')

    @mock.patch('requests.put')
    def test_registered_connection_error(self, mock):
        mock.side_effect = ConnectionError
        register_data = {
            'first_name': 'Test',
            'last_name': 'Account',
            'merchant_name': 'Test Merchant',
            'email': 'test@test.com',
            'password': 'test',
            'repeat_password': 'test'
        }
        request = self.client.post('/myapp/registered/', data=register_data)
        self.assertRedirects(request, '/myapp/broadcast/')

    def test_registered_key_error(self):
        self.clear_ads()
        mock_test = mock.patch.dict(os.environ, {'ARR_API_ID': '135p7z'})
        mock_test.start()
        register_data = {
            'first_name': 'Test',
            'last_name': 'Account',
            'merchant_name': 'Test Merchant',
            'email': 'test@test.com',
            'password': 'test',
            'repeat_password': 'test'
        }
        request = self.client.post('/myapp/registered/', data=register_data, follow=True)
        self.assertRedirects(request, '/myapp/broadcast/')
        mock_test.stop()

    def clear_ads(self):
        temp = json.dumps({})
        url = 'https://api.myjson.com/bins/135p7z'
        headers = {'Content-type': 'application/json'}
        return requests.put(url, data=temp, headers=headers)


class LogoutPageTest(TestSession, TestCase):

    def test_myapp_url_is_exist(self):
        response = Client().get('/myapp/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url_is_exist(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.get('/myapp/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_page_is_completed(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.get('/myapp/logout/')
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


class GetUserDataTest(TestCase):

    def test_get_user_data_success(self):
        user_temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
        user_arr = json.loads(requests.get(user_temp).content.decode())['user']
        email = 'test@test.com'
        user_data = {
            'name': 'Test Account',
            'first_name': 'Test',
            'last_name': 'Account',
            'merchant_name': 'test_merchant',
            'profile_picture': '',
            'email': 'test@test.com'
        }
        result = get_user_data(user_arr, email)
        self.assertEqual(result['name'], user_data['name'])
        self.assertEqual(result['first_name'], user_data['first_name'])
        self.assertEqual(result['last_name'], user_data['last_name'])
        self.assertEqual(result['merchant_name'], user_data['merchant_name'])
        self.assertEqual(result['email'], user_data['email'])

    def test_get_user_data_fail(self):
        user_temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
        user_arr = json.loads(requests.get(user_temp).content.decode())['user']
        email = 'failtest@test.com'
        user_data = {
            'name': '',
            'first_name': '',
            'last_name': '',
            'merchant_name': '',
            'profile_picture': '',
            'email': ''
        }
        result = get_user_data(user_arr, email)
        self.assertEqual(result['name'], user_data['name'])
        self.assertEqual(result['first_name'], user_data['first_name'])
        self.assertEqual(result['last_name'], user_data['last_name'])
        self.assertEqual(result['merchant_name'], user_data['merchant_name'])
        self.assertEqual(result['email'], user_data['email'])


class ProfilePageTest(TestSession, TestCase):

    def test_profile_page_is_exist(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.get('/myapp/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_page_redirects_if_not_signed_in(self):
        self.create_session()
        session = self.client.session
        session.save()
        response = self.client.get('/myapp/profile/')
        self.assertEqual(response.status_code, 302)


class EditProfileSuccessPageTest(TestSession, TestCase):

    def test_edit_profile_success_page_is_exist(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.get('/myapp/editSuccess/')
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_success_page_redirects_if_not_signed_in(self):
        self.create_session()
        session = self.client.session
        session.save()
        response = self.client.get('/myapp/editSuccess/')
        self.assertEqual(response.status_code, 302)


class EditProfilePageTest(TestSession, TestCase):

    def create_profile(self, img=''):
        user_data = {}
        user_data['first_name'] = 'Test'
        user_data['last_name'] = 'Account'
        user_data['merchant_name'] = 'test_merchant'
        user_data['profpic'] = img
        return user_data

    def test_edit_profile_page_is_exist(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.get('/myapp/editProfile/')
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_page_redirects_if_not_signed_in(self):
        self.create_session()
        session = self.client.session
        session.save()
        response = self.client.get('/myapp/editProfile/')
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_with_profpic(self):
        img = open('static/image/coba.jpeg', 'rb')
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.post('/myapp/editProfile/', self.create_profile(img))
        self.assertRedirects(response, '/editSuccess/')

    def test_edit_profile_without_profpic(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.post('/myapp/editProfile/', self.create_profile())
        self.assertRedirects(response, '/editSuccess/')

    @mock.patch('requests.put')
    def test_connection_error(self, mock):
        mock.side_effect = ConnectionError
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        response = self.client.post('/myapp/editProfile/', self.create_profile())
        self.assertRedirects(response, '/myapp/editProfile/response/')


class StatisticPageTest(TestSession, TestCase):

    def test_get_statistic_success(self):
        self.create_session()
        session = self.client.session
        session['email'] = 'test@test.com'
        session.save()
        url = reverse('statistic')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/template/statistic.html')
        # self.assertEqual()
