from django.urls import path


from .views import OrganizationListView, OrganizationDetailView


app_name = 'organizations'

urlpatterns = [

	path('', OrganizationListView.as_view(), name='list'),
	path('<int:pk>/', OrganizationDetailView.as_view(), name='detail'),

]



