from django.test import TestCase
from myapp.forms import RegisterForm, LoginForm

# Create your tests here.


class RegisterFormTest(TestCase):

    def test_valid_data(self):
        form = RegisterForm({
            'first_name': 'Citra',
            'last_name': 'Glory',
            'merchant_name': 'Toko Glory',
            'email': 'citra@example.com',
            'password': 'cicitcuit',
            'repeat_password': 'cicitcuit'
        })
        self.assertTrue(form.is_valid())
        reg = form.save()
        self.assertEqual(reg.first_name, 'Citra')
        self.assertEqual(reg.last_name, 'Glory')
        self.assertEqual(reg.merchant_name, 'Toko Glory')
        self.assertEqual(reg.email, 'citra@example.com')
        self.assertEqual(reg.password, 'cicitcuit')
        self.assertEqual(reg.repeat_password, 'cicitcuit')

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
            'email': 'citra@example.com',
            'password': 'cicitcuit'
        })
        self.assertTrue(form.is_valid())
        log = form.save()
        self.assertEqual(log.email, 'citra@example.com')
        self.assertEqual(log.password, 'cicitcuit')

    def test_blank_data(self):
        form = LoginForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['This field is required.'],
            'password': ['This field is required.']
        })
