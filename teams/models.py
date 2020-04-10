from django.db import models


from shared.models import BaseModel


class Team(BaseModel):
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField()
	website = models.URLField(null=True, blank=True)

	def __str__(self):
		return f'{self.name}'

	class Meta:
		ordering = ['-_total_servicehours', ]
