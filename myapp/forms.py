from django import forms
from .models import Register, Login


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Register
        fields = ('first_name', 'last_name', 'merchant_name',
                  'email', 'password', 'repeat_password')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['merchant_name'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['repeat_password'].required = True
        self.fields['password'].widget.attrs['required'] = 'required'
        self.fields['repeat_password'].widget.attrs['required'] = 'required'


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['password'].widget.attrs['required'] = 'required'
