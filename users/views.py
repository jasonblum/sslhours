from django.contrib import messages
from django.contrib.auth import get_user_model	
from django.shortcuts import render, get_object_or_404

from impersonate.views import stop_impersonate

User = get_user_model()



def detail(request, pk):
	user = get_object_or_404(User, pk=pk)
	coordinated_servicehours = user.coordinated_servicehours.select_related(
		'student', 'student__user', 'activity', 'school', 'team', 'activity__organization', 
		).prefetch_related(
		'school__ssl_coordinators'
		)
	return render(request, 'users/detail.html', {'user':user, 'coordinated_servicehours': coordinated_servicehours})


def stop_impersonate(request):
	messages.success(request, f'@{request.impersonator.username} is no longer impersonating @{request.user.username}!')
	return stop_impersonate(request)

