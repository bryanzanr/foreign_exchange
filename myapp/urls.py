from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from myapp import views

router = routers.DefaultRouter()
router.register(r'currency', views.CurrencyViewSet)
router.register(r'exchange', views.ExchangeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.ExchangeList.as_view(),
    name='exchange_list'),
    path('date/', views.ExchangeForm.as_view(),
    name='exchange_form'),
    path('variance/', views.ExchangeVariance.as_view(),
    name='exchange_variance'),
    path('daily/', views.DailyExchange.as_view(),
    name='daily_exchange'),
    path('track/', views.CustomCurrency.as_view(),
    name='custom_currency')
]
