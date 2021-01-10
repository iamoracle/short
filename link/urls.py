from django.contrib import admin
from django.urls import path

from .views import LinkView

urlpatterns = [
    path('add/', LinkView.as_view(), name="add_link"),
    path('delete/<str:slug>/<str:secret>', LinkView.as_view(), name="delete_link"),
]
