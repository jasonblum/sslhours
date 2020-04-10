from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

from .views import stop_impersonate, detail


app_name = 'users'

urlpatterns = [

    path('users/<int:pk>/', detail, name='detail'),

	path('stop_impersonate/', stop_impersonate, name='stop_impersonate'),

]
