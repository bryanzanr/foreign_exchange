from .models import Currency, Exchange
from .serializers import CurrencySerializer, ExchangeSerializer
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime


class ExchangeForm(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exchange_form.html'

    def get(self, request):
        return Response()

    def post(self, request):
        try:
            datetime.datetime.strptime(request.data[
            'exchange_date'], '%Y-%m-%d')
        except ValueError:
            return Response()
        request.session['exchange_date'] = request.data['exchange_date']
        return redirect('exchange_list')


class ExchangeList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exchange_list.html'

    def get(self, request):
        try:
            exchange_date = request.session['exchange_date']
        except KeyError:
            return redirect('exchange_form')
        currency_query = Currency.objects.raw('SELECT * FROM myapp_currency')
        result = []
        for currency in currency_query:
            queryset = {}
            queryset['currency_from'] = currency.currency_from
            queryset['currency_to'] = currency.currency_to
            exchange_query = Exchange.objects.raw('SELECT * FROM myapp_exchange'
            + ' WHERE currency_id_id = %s AND exchange_date > date %s - '
            + "interval '7 day'", [currency.id, exchange_date])
            count = 0
            counter = 0
            for exchange in exchange_query:
                if exchange.exchange_date == exchange_date:
                    queryset['exchange_rate'] = exchange.exchange_date
                count += exchange.exchange_rate
                counter += 1
            queryset['avg'] = count/7
            if counter < 7:
                queryset['exchange_rate'] = 'insufficient data'
                queryset['avg'] = ''
            result.append(queryset)
        return Response({'exchanges': result})


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows currency to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ExchangeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows exchange to be viewed or edited.
    """
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
