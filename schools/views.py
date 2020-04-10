from django.shortcuts import render
from django.views.generic import DetailView

from stronghold.views import StrongholdPublicMixin, public


from .models import School



@public
class SchoolDetailView(StrongholdPublicMixin, DetailView):
	model = School
	template_name = 'schools/detail.html'
	context_object_name = 'school'


@public
def list_schools(request):
	schools = School.objects.filter(is_active=True).prefetch_related('ssl_coordinators')
	return render(request, 'schools/list.html', {'schools':schools})

@public
def grade(request):
	pass
