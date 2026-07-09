from django.urls import path
from .views import dashboard_view, mobil_view, LokatsiyaYangilashAPI, XaritaMalumotlariAPI

urlpatterns = [
    # dashboard/ joyiga bo'sh joy qoldirdik, bu bosh sahifa (/) degani:
    path('', dashboard_view, name='dashboard'),

    path('mobil/', mobil_view, name='mobil'),
    path('api/update/', LokatsiyaYangilashAPI.as_view(), name='api_update'),
    path('api/map-data/', XaritaMalumotlariAPI.as_view(), name='api_map_data'),
]