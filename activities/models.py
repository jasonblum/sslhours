from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from shared.models import BaseModel
from organizations.models import Organization



class Activity(BaseModel):
	name = models.CharField(max_length=120)
	description = models.TextField()
	organization = models.ForeignKey(
		Organization,
		on_delete=models.PROTECT,
		related_name='activities'
	)
	manager = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name='activities'
	)
	managers = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		related_name='managed_activities',
		blank=True
	)

	def __str__(self):
		return f'{self.name} ({self.organization})'

	def can_manage(self, user):
		return user == self.manager or user in self.managers.all() or user.is_superuser

	@property
	def managers_names_hyperlinked(self):
		return mark_safe(', '.join([self.manager.hyperlinked_name] + [m.hyperlinked_name for m in self.managers.all()]))
	
	class Meta:
		verbose_name = 'Activity'
		verbose_name_plural = 'Activities'
		ordering = ['-_total_servicehours', ]
		unique_together = ['name', 'organization', ]
