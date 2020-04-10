import random
from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.db.models import Sum
from django.urls import reverse

from shared.models import BaseModel
from shared.utilities import get_object_or_None

from schools.models import School
from teams.models import Team



def pick_random_avatar():
	return random.choice(settings.AVATARS)


class Student(BaseModel):
	username = models.CharField(max_length=50, unique=True, help_text='Defaults to mcps_id.')
	mcps_id = models.PositiveIntegerField(unique=True)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	grade = models.PositiveSmallIntegerField(
		choices=settings.GRADE_CHOICES, 
		null=True
	)
	school = models.ForeignKey(School, on_delete=models.PROTECT, null=True, related_name='students')
	team = models.ForeignKey(
		Team,
		on_delete=models.PROTECT,
		related_name='students',
		null=True, blank=True
	)
	phone = models.CharField(max_length=14, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	first_period_teacher = models.CharField(max_length=30, null=True, blank=True)
	parent_name = models.CharField(max_length=30, null=True, blank=True)
	parent_phone = models.CharField(max_length=14, null=True, blank=True)
	parent_phone_other = models.CharField(max_length=14, null=True, blank=True)
	avatar = models.CharField(max_length=50, default=pick_random_avatar)

	_beginning_total_servicehour_balance = models.DecimalField(default=Decimal(0.0), max_digits=6, decimal_places=1, help_text='Beginning balance outside of SSLHours, to be credited only by admin.')

	def __str__(self):
		return self.username

	class Meta:
		ordering = ['-_total_servicehours', ]

	@transaction.atomic
	def save(self, *args, **kwargs): 
		#Update any servicehours hanging out there.
		if hasattr(self, 'servicehours'):
			self.servicehours.exclude(_status='credited').update(
				school = self.school,
				grade = self.grade,
				team = self.team
			)

		if not self.username:
			self.username = str(self.mcps_id)
		super(Student, self).save(*args, **kwargs) 

	def get_absolute_url(self):
		return reverse('student_cv', args=[self.username])

	@property
	def beginning_total_servicehour_balance(self):
		return self._beginning_total_servicehour_balance
	

	@property
	def activities(self):
		return self.servicehours.values_list('activity', flat=True).distinct()
	
	@property
	def organizations(self):
		return self.servicehours.values_list('activity__organization', flat=True).distinct()
	

class Snapshot(models.Model):
	dt_created = models.DateTimeField(auto_now_add=True)
	student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='snapshots')
	position = models.PositiveSmallIntegerField()
	out_of = models.PositiveSmallIntegerField()
	leaderboard = models.CharField(max_length=14, choices=settings.LEADERBOARD_CHOICES)

	class Meta:
		ordering = ['-dt_created', ]






