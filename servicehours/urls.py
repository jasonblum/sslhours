from django.urls import path
from django.views.generic import TemplateView

from .views import list_servicehours, detail, edit, pdf



app_name = 'servicehours'


urlpatterns = [

	path('', list_servicehours, name='list'),
	path('<int:pk>/', detail, name='detail'),
	path('edit/<int:pk>/', edit, name='edit'),
	path('pdf/<int:pk>/', pdf, name='pdf'),
]


