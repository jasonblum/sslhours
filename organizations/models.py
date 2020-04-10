from django.conf import settings
from django.db import models
from django.urls import reverse

from shared.models import BaseModel


class Organization(BaseModel):
	name = models.CharField(max_length=100, unique=True)
	ein = models.CharField(max_length=9, unique=True)
	phone = models.CharField(max_length=14)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=40)
	state = models.CharField(max_length=2)
	zip_code = models.CharField(max_length=10)
	email = models.EmailField()
	description = models.TextField()
	website = models.URLField(null=True, blank=True)
	manager = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name='organizations'
	)
	def __str__(self):
		return f'{self.name}'

	@property
	def users_who_can_manage(self, user):
		return self.manager


	class Meta:
		ordering = ['-_total_servicehours', ]
