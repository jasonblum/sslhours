from stronghold.decorators import public
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import apnumber
from django.db.models import Sum
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404, render, redirect



from students.models import Student
from schools.models import School
from activities.models import Activity
from organizations.models import Organization
from servicehours.models import ServiceHour
from teams.models import Team


from shared.templates.help_text import HELP_TEXT




@public
def home(request):

	students = Student.objects.all()
	schools = School.objects.all()
	high_schools = schools.filter(school_type='high').all()
	middle_schools = schools.filter(school_type='middle').all()
	activities = Activity.objects.all()
	organizations = Organization.objects.all()
	teams = Team.objects.all()

	servicehour_count = ServiceHour.objects.filter(_status='credited').count()

	stats = mark_safe(f'''
	<button type="button" class="highlight btn btn-outline-success btn-sm">{teams.count()}</button> teams of
	<button type="button" class="highlight btn btn-outline-danger btn-sm">{students.count()}</button> students from 
	<button type="button" class="highlight btn btn-outline-warning btn-sm">{high_schools.count()+middle_schools.count()}</button> schools have completed
	<button type="button" class="highlight btn btn-outline-info btn-sm">{servicehour_count}</button> <a href="https://www.montgomeryschoolsmd.org/departments/ssl/">Student Service Learning</a> hours in
	<button type="button" class="highlight btn btn-outline-primary btn-sm">{activities.count()}</button> activities for
	<button type="button" class="highlight btn btn-outline-dark btn-sm">{organizations.count()}</button> organizations
	to date!''')

	return render(request, 'home.html', {
		'stats': stats,
		'students' : students[:5],
		'middle_schools' : middle_schools[:5],
		'high_schools' : high_schools[:5],
		'teams' : teams[:5],
		'activities' : activities[:5],
		'organizations' : organizations[:5],
	})

@public
def help(request):
	return render(request, 'help.html', {'HELP_TEXT' : HELP_TEXT})



@public
def trigger_error(request):
	division_by_zero = 1 / 0

