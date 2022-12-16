from django.urls import path

from .views import LocalizationView, LocalizationPart

urlpatterns = [
    path(
        'localization/',
        LocalizationView.as_view(),
        name='localization_view'
    ),
    path(
        'localization-part/<str:antenna>',
        LocalizationPart.as_view(),
        name='localization_part'
    )
]