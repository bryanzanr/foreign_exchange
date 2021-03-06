from .forms import CurrencyForm
from .models import Currency, Exchange
from .serializers import CurrencySerializer, ExchangeSerializer
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime, sys


class ExchangeVariance(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exchange_variance.html'

    def get(self, request):
        return Response()

    def post(self, request):
        currency_from = request.data['currency_from']
        currency_to = request.data['currency_to']
        if len(currency_from) < 3 or len(currency_to) < 3:
            return Response({'failed': True})
        querydict = Exchange.objects.raw('SELECT * FROM myapp_currency C, '
        + 'myapp_exchange E WHERE E.currency_id = C.id AND C.currency_from'
        + '= %s AND C.currency_to = %s AND E.exchange_date > current_date - '
        + "INTERVAL '7 day'", [currency_from, currency_to])
        max = sys.float_info.min
        min = sys.float_info.max
        count = 0
        counter = 0
        for exchange in querydict:
            if exchange.exchange_rate > max:
                max = exchange.exchange_rate
            if exchange.exchange_rate < min:
                min = exchange.exchange_rate
            count += exchange.exchange_rate
            counter += 1
        if counter > 0:
            return Response({'exchange': {'average': count/counter,
            'variance': max - min}, 'exchanges': querydict,
            'currency_from': currency_from,
            'currency_to': currency_to})
        else:
            return Response({'failed': True})


class ExchangeForm(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exchange_form.html'

    def get(self, request):
        try:
            exchange_date = request.session['exchange_date']
            return Response({'exchange_date': exchange_date})
        except KeyError:
            return Response()

    def post(self, request):
        try:
            datetime.datetime.strptime(request.data[
            'exchange_date'], '%Y-%m-%d')
        except ValueError:
            return Response({'failed': True})
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
            + ' WHERE currency_id = %s AND exchange_date > date %s - '
            + "INTERVAL '7 day'", [currency.id, exchange_date])
            count = 0
            counter = 0
            for exchange in exchange_query:
                if str(exchange.exchange_date) == exchange_date:
                    queryset['exchange_rate'] = exchange.exchange_rate
                count += exchange.exchange_rate
                counter += 1
            queryset['avg'] = count/7
            if counter < 7:
                queryset['exchange_rate'] = 'insufficient data'
                queryset['avg'] = ''
            result.append(queryset)
        return Response({'exchanges': result})

    def post(self, request):
        exchange_date = request.POST.get('exchange_date', '')
        if exchange_date == "":
            return JsonResponse({'status': False}, status=200)
        currency_query = Currency.objects.raw('SELECT * FROM myapp_currency')
        result = []
        for currency in currency_query:
            queryset = {}
            queryset['currency_from'] = currency.currency_from
            queryset['currency_to'] = currency.currency_to
            exchange_query = Exchange.objects.raw('SELECT * FROM myapp_exchange'
            + ' WHERE currency_id = %s AND exchange_date > date %s - '
            + "INTERVAL '7 day'", [currency.id, exchange_date])
            count = 0
            counter = 0
            for exchange in exchange_query:
                if str(exchange.exchange_date) == exchange_date:
                    queryset['exchange_rate'] = exchange.exchange_rate
                count += exchange.exchange_rate
                counter += 1
            queryset['avg'] = count/7
            if counter < 7:
                queryset['exchange_rate'] = 'insufficient data'
                queryset['avg'] = ''
            result.append(queryset)
        return JsonResponse({'status': True,
        'exchanges': result}, status=200)


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


class DailyExchange(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'daily_exchange.html'

    def get(self, request):
        return Response()

    def post(self, request):
        exchange_date = request.data['exchange_date']
        currency_from = request.data['currency_from']
        currency_to = request.data['currency_to']
        exchange_rate = request.data['exchange_rate']
        querydict = Exchange.objects.raw('SELECT * FROM myapp_currency C, '
        + 'myapp_exchange E WHERE E.currency_id = C.id AND C.currency_from'
        + '= %s AND C.currency_to = %s', [currency_from, currency_to])
        for exchange in querydict:
            data = Currency.objects.get(currency_from=currency_from,
            currency_to=currency_to)
            daily = Exchange(exchange_date=exchange_date,
            exchange_rate=exchange_rate)
            daily.currency_id = data.id
            if Exchange.objects.filter(exchange_date=exchange_date,
            currency=data).exists():
                return Response({'exchange_date': exchange_date,
                'currency_from': currency_from,
                'currency_to': currency_to,
                'exchange_rate': exchange_rate,
                'duplicate': True})
            daily.save()
            return Response({'success': True})
        return Response({'exchange_date': exchange_date,
        'currency_from': currency_from,
        'currency_to': currency_to,
        'exchange_rate': exchange_rate,
        'failed': True})


class CustomCurrency(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'custom_currency.html'

    def get(self, request):
        return Response()

    def post(self, request):
        form = CurrencyForm(request.POST)
        if form.is_valid():
            if Currency.objects.filter(currency_from=request
            .data['currency_from'], currency_to=request
            .data['currency_to']).exists():
                return Response({'failed': True})
            form.insert()
            return Response({'success': True})
        else:
            return Response({'currency_from': request.data['currency_from'],
            'currency_to': request.data['currency_to'],
            'success': False})


class CurrencyDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'currency_delete.html'

    def get(self, request):
        try:
            status = request.session['delete']
            del request.session['delete']
        except KeyError:
            status = False
        querydict = Currency.objects.raw('SELECT * FROM myapp_currency')
        return Response({'currencies': querydict, 'success': status})

def currency_delete(request, currency_id=None):
    currency = Currency.objects.get(id=currency_id)
    currency.delete()
    request.session['delete'] = True
    return redirect('remove_currency')

def add_currency(request):
    if request.method == 'POST':
        currency_from = request.POST.get('currency_from', '')
        currency_to = request.POST.get('currency_to', '')
        if Currency.objects.filter(currency_from=currency_from,
        currency_to=currency_to).exists():
            return JsonResponse({'status': False,
            'message': 'Currency existed'}, status=200)
        elif len(currency_from) < 3 or len(currency_to) < 3:
            return JsonResponse({'status': False,
            'message': 'Wrong Currency Format'}, status=200)
        currency = Currency(currency_from=currency_from,
        currency_to=currency_to)
        currency.save()
        return JsonResponse({'status': True,
        'message': 'Currency Inserted'}, status=200)
    return JsonResponse({'status': False,
    'message': 'Not POST method'}, status=404)

def add_exchange(request):
    if request.method == 'POST':
        exchange_date = request.POST.get('exchange_date', '')
        currency_from = request.POST.get('currency_from', '')
        currency_to = request.POST.get('currency_to', '')
        exchange_rate = request.POST.get('exchange_rate', '')
        querydict = Exchange.objects.raw('SELECT * FROM myapp_currency C, '
        + 'myapp_exchange E WHERE E.currency_id = C.id AND C.currency_from'
        + '= %s AND C.currency_to = %s', [currency_from, currency_to])
        print(querydict)
        for exchange in querydict:
            data = Currency.objects.get(currency_from=currency_from,
            currency_to=currency_to)
            daily = Exchange(exchange_date=exchange_date,
            exchange_rate=exchange_rate)
            daily.currency_id = data.id
            if Exchange.objects.filter(exchange_date=exchange_date,
            currency=data).exists():
                return JsonResponse({'status': False,
                'message': 'Daily Exchange Existed'}, status=200)
            daily.save()
            return JsonResponse({'status': True,
            'message': 'Exchange Inserted'}, status=200)
        return JsonResponse({'status': False,
        'message': 'Please Insert Currency First'}, status=200)
    return JsonResponse({'status': False,
    'message': 'Not POST method'}, status=404)

def get_variance(request):
    if request.method == 'POST':
        currency_from = request.POST.get('currency_from', '')
        currency_to = request.POST.get('currency_to', '')
        if len(currency_from) < 3 or len(currency_to) < 3:
            return JsonResponse({'status': False,
            'message': 'Wrong Currency Format'}, status=200)
        querydict = Exchange.objects.raw('SELECT * FROM myapp_currency C, '
        + 'myapp_exchange E WHERE E.currency_id = C.id AND C.currency_from'
        + '= %s AND C.currency_to = %s AND E.exchange_date > current_date - '
        + "INTERVAL '7 day'", [currency_from, currency_to])
        max = sys.float_info.min
        min = sys.float_info.max
        count = 0
        counter = 0
        result = []
        for exchange in querydict:
            temp = {}
            if exchange.exchange_rate > max:
                max = exchange.exchange_rate
            if exchange.exchange_rate < min:
                min = exchange.exchange_rate
            count += exchange.exchange_rate
            temp['exchange_date'] = exchange.exchange_date
            temp['exchange_rate'] = exchange.exchange_rate
            result.append(temp)
            counter += 1
        if counter > 0:
            return JsonResponse({'status': True,
            'exchange': {'average': count/counter,
            'variance': max - min}, 'exchanges': result,
            'currency_from': currency_from,
            'currency_to': currency_to})
        else:
            return JsonResponse({'status': False,
            'message': 'Please insert daily exchange first'})

def remove_currency(request):
    if request.method == 'POST':
        currency_from = request.POST.get('currency_from', '')
        currency_to = request.POST.get('currency_to', '')
        if len(currency_from) < 3 or len(currency_to) < 3:
            return JsonResponse({'status': False,
            'message': 'Wrong Currency Format'}, status=200)
        elif Currency.objects.filter(currency_from=currency_from,
        currency_to=currency_to).exists():
            currency = Currency.objects.get(currency_from=currency_from,
            currency_to=currency_to)
            currency.delete()
            return JsonResponse({'status': True,
            'message': 'Currency Deleted'}, status=200)
        else:
            return JsonResponse({'status': False,
            'message': 'Currency not found'}, status=200)
    return JsonResponse({'status': False,
    'message': 'Not POST method'}, status=404)
