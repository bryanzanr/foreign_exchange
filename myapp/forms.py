from django import forms
from .models import Register, Login, Ads


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


class AdsForm(forms.ModelForm):

    class Meta:
        model = Ads
        fields = ('title', 'desc', 'address', 'latitude', 'longitude', 'img')
        # fields = ('title', 'desc', 'fileUpload')
    title = forms.CharField(label='Title', required=True, max_length=100)
    desc = forms.CharField(label='Description', required=True, max_length=300)
    address = forms.CharField(label='Address', required=False, max_length=45)
    latitude = forms.CharField(label='Latitude', required=False, max_length=30)
    longitude = forms.CharField(label='Longitude', required=False, max_length=30)
    img = forms.URLField(label='Image', required=False)
