from django.urls import path


from .views import list_schools, SchoolDetailView, grade

app_name = 'schools'

urlpatterns = [

	path('', list_schools, name='list'),
	path('<int:pk>/', SchoolDetailView.as_view(), name='detail'),
	path('grade/<int:pk>/', grade, name='grade'),

]



