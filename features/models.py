from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe


class Feature(models.Model):
	STATUS_CHOICES = (
		('open', 'Open'),
		('completed', 'Completed'),
		('closed', 'Closed'),
	)

	name = models.CharField(max_length=254)
	discussion = models.TextField()
	_tally = models.SmallIntegerField(default=0)
	status = models.CharField(max_length=10, default=STATUS_CHOICES[0][0])
	outcome = models.TextField()

	def __str__(self):
		return f'{self.name}'

	@property
	def upvoters(self):
		return [vote.user for vote in self.votes.filter(upordown='up')]
	
	@property
	def downvoters(self):
		return [vote.user for vote in self.votes.filter(upordown='down')]	

	def save(self, *args, **kwargs): 
		self._tally = self.votes.filter(upordown='up').count() - self.votes.filter(upordown='down').count()
		super(Feature, self).save(*args, **kwargs) 

	class Meta:
		ordering = ['-_tally', ]

	@property
	def tally(self):
		return self._tally
	



class Vote(models.Model):
	feature = models.ForeignKey(
		Feature,
		on_delete=models.PROTECT,
		related_name='votes'
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name='votes'
	)
	upordown = models.CharField(max_length=4, choices=(('up', 'up'), ('down', 'down'), ))

	def __str__(self):
		return f'{self.upordown} on {self.feature} by {self.user}'		


