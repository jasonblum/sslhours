from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from stronghold.decorators import public

from .models import Feature, Vote


@public
def list_features(request):
	features = Feature.objects.all()
	return render(request, 'features/list.html', {'features' : features})


def vote(request, pk, upordown):
	feature = get_object_or_404(Feature, pk=pk)
	vote, created = Vote.objects.update_or_create(
		feature = feature,
		user = request.user,
		defaults = {'upordown' : upordown }
	)
	feature.save()
	messages.success(request, f'You voted {upordown.upper()} on the feature "{feature}"!')
	return redirect('features:list')