from django.urls import path

from .views import LocalizationView

urlpatterns = [
    path(
        'localization/',
        LocalizationView.as_view(),
        name='localization_view'
    )
]