from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import ListView, DetailView

from stronghold.decorators import public
from stronghold.views import StrongholdPublicMixin

from shared.utilities import get_object_or_None

from .models import Activity

from students.models import Student
from servicehours.models import ServiceHour


class ActivityListView(StrongholdPublicMixin, ListView):
	model = Activity
	template_name = 'activities/list.html'
	context_object_name = 'activities'


def detail(request, pk):
	activity = get_object_or_404(Activity, pk=pk)

	can_manage = activity.can_manage(request.user)

	if can_manage: 
		mcps_ids = Student.objects.filter(is_active=True).values_list('mcps_id', flat=True)
	else:
		mcps_ids = []

	servicehours = ServiceHour.objects.filter(activity=activity).select_related('student', 'student__user', 'school',  )

	return render(request, 'activities/detail.html', 
		{'activity': activity, 
		'can_manage': can_manage, 
		'mcps_ids':mcps_ids,
		'servicehours': servicehours})


def checkin(request):
	mcps_id = int(request.POST.get('mcps_id', 0))
	activity_pk = int(request.POST.get('activity_pk', 0))
	activity = get_object_or_404(Activity, pk=activity_pk)

	if not activity.can_manage(request.user):
		raise PermissionDenied('You are not a manager of this activity.')

	student, created = Student.objects.get_or_create(mcps_id=mcps_id)

	if ServiceHour.objects.filter(student=student, activity=activity, end_time__isnull=True).exists():
		messages.warning(request, f'Student with MCPS ID {mcps_id} is already checked in to this activity.')
		return redirect(activity.get_absolute_url())

	servicehour = ServiceHour.objects.create(
		student = student,
		activity = activity,
		start_time = timezone.now()
	)

	if hasattr(student, 'user'):
		messages.success(request, mark_safe(f'Student {student.hyperlinked_name} has been checked IN!'))
	else:
		messages.success(request, mark_safe(f'Student {student.hyperlinked_name} has been checked IN, but please remind them they will need to create an account here to claim this MCPS ID.'))

	return redirect(activity.get_absolute_url())


def checkout(request, pk):
	servicehour = get_object_or_404(ServiceHour, pk=pk)

	if not servicehour.activity.can_manage(request.user):
		raise PermissionDenied('You are not a manager of this activity.')

	servicehour.end_time = timezone.now()

	seconds = (servicehour.end_time - servicehour.start_time).seconds
	if seconds < 60:
		messages.warning(request, f'Unable to credit SSL time for less than a minute.')
		return redirect('activities:detail', servicehour.activity.pk)

	servicehour._total = seconds/60/60
	servicehour.save()

	if hasattr(servicehour.student, 'user'):
		messages.success(request, mark_safe(f'Student {servicehour.student.hyperlinked_name} has been checked OUT!'))
	else:
		messages.success(request, mark_safe(f'Student {servicehour.student.hyperlinked_name} has been checked OUT, but please remind them they will need to create an account here to claim this MCPS ID.'))

	return redirect(servicehour.activity.get_absolute_url())






