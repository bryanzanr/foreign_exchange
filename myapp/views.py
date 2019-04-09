from .models import Currency, Exchange
from .serializers import CurrencySerializer, ExchangeSerializer
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
            datetime.datetime.strptime(request.data, '%Y-%m-%d')
        except ValueError:
            return
        return redirect('exchange_list')


class ExchangeList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exchange_list.html'

    def get(self, request):
        queryset = Exchange.objects.raw('select * FROM myapp_currency C, '
        + 'myapp_exchange E where E.currency_id_id = C.id')
        return Response({'exchanges': queryset})


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ExchangeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
