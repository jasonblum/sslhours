from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.db.models import Sum
from django.urls import reverse
from django.utils.safestring import mark_safe

from shared.models import BaseModel
from schools.models import School
from activities.models import Activity
from students.models import Student
from teams.models import Team


class ServiceHour(models.Model):

	STATUS_CHOICES = (
		('incomplete', 'Incomplete'),
		('pending', 'Pending'),
		('credited', 'Credited'),
	)

	start_time = models.DateTimeField()
	end_time = models.DateTimeField(blank=True, null=True)
	reflections = models.TextField(blank=True, null=True)
	crediting_SSL_coordinator = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name='credited_servicehours',
		null=True, blank=True
	)
	student = models.ForeignKey(
		Student,
		on_delete=models.PROTECT,
		related_name='servicehours'
	)
	activity = models.ForeignKey(
		Activity,
		on_delete=models.PROTECT,
		related_name='servicehours',
	)
	school = models.ForeignKey(
		School,
		on_delete=models.PROTECT,
		related_name='servicehours',
		null=True, blank=True,
		help_text='School of student when this hour was credited.'
	)
	grade = models.PositiveSmallIntegerField(
		choices=settings.GRADE_CHOICES, 
		null=True, blank=True
	)
	team = models.ForeignKey(
		Team,
		on_delete=models.PROTECT,
		related_name='servicehours',
		null=True, blank=True,
		help_text=f'You can associate this time with a team or club. If you don\t see them here, email {settings.SITE_SUPPORT_EMAIL}.'
	)
	_status = models.CharField(max_length=10, default=STATUS_CHOICES[0][0], editable=False)
	_total = models.DecimalField(default=Decimal(0.0), max_digits=4, decimal_places=1, editable=False)

	dt_created = models.DateTimeField(auto_now_add=True)
	dt_updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Service Hour'
		verbose_name_plural = 'Service Hours'
		ordering = ['-_total', ]

	def __str__(self):
		return f'Service Hour for {self.student} at activity {self.activity}'

	@property
	def users_who_can_credit(self):
		return list(self.school.ssl_coordinators.all()) if self.school else []

	@property
	def users_who_can_manage(self):
		return self.users_who_can_credit + [getattr(self.student, 'user', None)]

	@property
	def total(self):
		return self._total

	@property
	def status(self):
		return self._status

	@property
	def student_has_user(self):
		return hasattr(self, 'student')

	def delete(self):
		if self._status == 'credited':
			raise PermissionDenied('Cannot be deleted if already credited.')

	@transaction.atomic
	def save(self, *args, **kwargs): 
		#TODO need to review all of this
		#AND LOTS OF TESTS AROUND THESE CALCULATIONS AND STATUS SETTING...
		#TODO need to review all of this
		#AND LOTS OF TESTS AROUND THESE CALCULATIONS AND STATUS SETTING...
		#TODO need to review all of this
		#AND LOTS OF TESTS AROUND THESE CALCULATIONS AND STATUS SETTING...
		#TODO need to review all of this
		#AND LOTS OF TESTS AROUND THESE CALCULATIONS AND STATUS SETTING...
		#TODO need to review all of this
		#AND LOTS OF TESTS AROUND THESE CALCULATIONS AND STATUS SETTING...

		if self.end_time:
			seconds = float((self.end_time - self.start_time).seconds)
			if seconds < 60:
				raise Exception('A Service Hour must last at least 15 minutes...')
			else:
				self._total = str(round(seconds/60/60, 2))

		if self.crediting_SSL_coordinator:
			self._status = 'credited'
		elif self.end_time and self._total and self.reflections:
			self._status = 'pending'
		else:
			self._status = 'incomplete'

		super(ServiceHour, self).save(*args, **kwargs) 

		#Save related models to have them update their service hour balance.
		self.student.save()
		self.activity.save()
		self.activity.organization.save()
		if self.school:
			self.school.save()
		if self.team:
			self.team.save()



class Comment(models.Model):
	dt_created = models.DateTimeField(auto_now_add=True)
	comment = models.TextField(help_text='Leave a comment for your SSL coordinator...')
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name='comments'
	)
	servicehour = models.ForeignKey(
		ServiceHour,
		on_delete=models.PROTECT,
		related_name='comments'
	)

	def __str__(self):
		return f'Comment on {self.servicehour}'