from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe


from shared.models import BaseModel


class School(BaseModel):
	mcps_school_id = models.PositiveSmallIntegerField(unique=True)
	name = models.CharField(max_length=50)
	school_type = models.CharField(max_length=6, choices=settings.SCHOOL_TYPE_CHOICES)
	address = models.CharField(max_length=100, unique=True)
	city = models.CharField(max_length=40)
	zip_code = models.CharField(max_length=10)
	phone = models.CharField(max_length=14, unique=True)
	ssl_coordinators = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		related_name='ssl_coordinated_schools',
		blank=True
	)

	class Meta:
		unique_together = ['name', 'school_type']
		ordering = ['-_total_servicehours', ]

	def __str__(self):
		return f'{self.name} {self.get_school_type_display()}'

	@property
	def ssl_coordinators_names_hyperlinked(self):
		return mark_safe(', '.join([s.hyperlinked_name for s in self.ssl_coordinators.all()]))