from django.urls import path

from .views import ActivityListView, detail, checkin, checkout


app_name = 'activities'

urlpatterns = [

	path('', ActivityListView.as_view(), name='list'),
	path('<int:pk>/', detail, name='detail'),

	path('checkin/', checkin, name='checkin'),
	path('checkout/<int:pk>/', checkout, name='checkout'),

]