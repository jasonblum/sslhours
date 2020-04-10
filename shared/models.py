import random
from decimal import Decimal
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.db.models import Sum
from django.urls import reverse
from django.utils.safestring import mark_safe





class BaseModel(models.Model):
	dt_created = models.DateTimeField(auto_now_add=True)
	dt_updated = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)

	_total_servicehours = models.DecimalField(default=Decimal(0.0), max_digits=12, decimal_places=1, editable=False)


	@transaction.atomic
	def save(self, *args, **kwargs): 
		#Update service hour balance
		if self.__class__.__name__ == 'Organization':
			total_servicehours = sum([
				Decimal(activity.servicehours.filter(_status='credited').aggregate(Sum('_total'))['_total__sum'] or 0.0)
				for activity in self.activities.all()
			])
		else:
			total_servicehours = Decimal(self.servicehours.filter(_status='credited').aggregate(Sum('_total'))['_total__sum'] or 0.0)
		
		if self.__class__.__name__ == 'Student':
			total_servicehours += self._beginning_total_servicehour_balance

		self._total_servicehours = total_servicehours
		super(BaseModel, self).save(*args, **kwargs) 






	class Meta:
		abstract = True

	def delete(self):
		raise PermissionDenied('This class of data cannot be deleted, only made inactive (is_active=False)')

	def get_absolute_url(self):
		return reverse(f'{self._meta.app_label}:detail', args=[self.pk])

	@property
	def hyperlinked_name(self):
		return mark_safe(f'<a href="{self.get_absolute_url()}">{self}</a>')

	@property
	def type(self):
		return self.__class__.__name__

	@property
	def total_servicehours(self):
		return self._total_servicehours


