from django.views.generic import ListView, DetailView

from stronghold.views import StrongholdPublicMixin


from .models import Team



class TeamDetailView(StrongholdPublicMixin, DetailView):
	model = Team
	template_name = 'teams/detail.html'
	context_object_name = 'team'


class TeamListView(StrongholdPublicMixin, ListView):
	model = Team
	template_name = 'teams/list.html'
	context_object_name = 'teams'

