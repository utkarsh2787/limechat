# frontend/urls.py

from django.urls import path
from frontend.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='frontend-index'),
]
