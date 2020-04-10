from django.views.generic import ListView, DetailView

from stronghold.views import StrongholdPublicMixin

from .models import Organization


class OrganizationListView(StrongholdPublicMixin, ListView):
	model = Organization
	template_name = 'organizations/list.html'
	context_object_name = 'organizations'


class OrganizationDetailView(StrongholdPublicMixin, DetailView):
	model = Organization
	template_name = 'organizations/detail.html'
	context_object_name = 'organization'
