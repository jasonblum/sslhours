from django import forms
from django.forms import ModelForm, CharField

from .models import ServiceHour, Comment


class ServiceHourForm(ModelForm):
	class Meta:
		model = ServiceHour
		fields = ('reflections', 'team', )


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('comment', )

	comment = forms.CharField(required=False)
