from django.contrib import admin
from django.urls import path

from .views import LinkView, RedirectView

urlpatterns = [
    path('add/', LinkView.as_view(), name="add_link"),
    path('<str:slug>/<str:secret>', LinkView.as_view(), name="delete_link"),
    path('<str:slug>', RedirectView.as_view(), name="redirect_link"),
]
