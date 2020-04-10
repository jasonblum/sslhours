from django.conf import settings
from django.contrib import messages
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404

from stronghold.views import public, StrongholdPublicMixin

from shared.utilities import get_object_or_None

from .models import Student, Snapshot
from .forms import StudentForm, ClaimMCPSIDForm



@public
def student_cv(request, slug):
	student = get_object_or_404(Student, username=slug, is_active=True)
	return render(request, 'students/cv.html', {'student':student})


@public
def list_students(request):
	students = Student.objects.filter(is_active=True).select_related('school','user')
	return render(request, 'students/list.html', {'students':students})


def edit(request):
	if not request.user.student:
		messages.warning(request, f'You have not claimed an MCPS Student ID, and so have no student to manage.')
		return redirect('home')

	form = StudentForm(request.POST or None, instance=request.user.student)
	if request.POST and form.is_valid():
		student = form.save()
		messages.success(request, f'Student has been saved.')
		return redirect(student.get_absolute_url())
	return render(request, 'students/edit.html', {'form': form, 'student': request.user.student, 'URL_TO_OFFICIAL_SSL_PDF': settings.URL_TO_OFFICIAL_SSL_PDF })


def claim(request):
	if request.user.student:
		messages.success(request, f'You already have a student: {request.user.student}.')
		return redirect('home')

	form = ClaimMCPSIDForm(request.POST or None)
	if request.POST and form.is_valid():
		student, created = Student.objects.get_or_create(mcps_id=form.cleaned_data['mcps_id'])
		if created:
			request.user.student = student
			request.user.save()
			messages.success(request, f'Student has been created!')
			return redirect('home')
		else:
			messages.success(request, f'That MCPS ID has already been claimed.  If this is your MCPS ID, please contact us immediately.')
			return redirect('home')

	return render(request, 'students/claim.html', {'form': form})


def snapshot(request, leaderboard):
	if not request.user.student:
		messages.success(request, 'You are not a student.')
		return redirect('home')

	Snapshot.objects.create(
		student = request.user.student,
		position = 1,
		out_of = 10,
		leaderboard = leaderboard
	)

	messages.success(request, f'Snapshot added to your profile.')
	return redirect(request.user.student.get_absolute_url())





def avatars(request):
	return render(request, 'students/avatars.html', {'avatars':settings.AVATARS})


def select_avatar(request, avatar):
	request.user.student.avatar = avatar
	request.user.student.save()
	return redirect(request.user.student.get_absolute_url())


