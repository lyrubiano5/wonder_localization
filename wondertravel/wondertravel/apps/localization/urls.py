from django.urls import path

from .views import ViewLocalization

urlpatterns = [
    path('localization/', ViewLocalization, name='localization_view')
]