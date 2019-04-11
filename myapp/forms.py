from django import forms
from .models import Currency

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'
    currency_from = forms.CharField(min_length=3, max_length=3, required=True)
    currency_to = forms.CharField(min_length=3, max_length=3, required=True)

    def insert(self):
        currency = Currency(currency_from=self.data['currency_from'],
        currency_to=self.data['currency_to'])
        currency.save()
