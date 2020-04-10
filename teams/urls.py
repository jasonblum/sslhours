from django.urls import path

from .views import TeamDetailView, TeamListView


app_name = 'teams'

urlpatterns = [

	path('', TeamListView.as_view(), name='list'),
	path('<int:pk>/', TeamDetailView.as_view(), name='detail'),

]