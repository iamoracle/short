from .views import LinkView

from django.urls import path

urlpatterns = [
    path('', LinkView.as_view()),
]
