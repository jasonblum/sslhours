from django.conf import settings
from django.urls import path, re_path

from .views import list_students, avatars, select_avatar, edit, claim, snapshot


app_name = 'students'

urlpatterns = [

	path('', list_students, name='list'),

	path('edit/', edit, name='edit'),

	path('claim/', claim, name='claim'),

    re_path(r'^snapshot/(?P<leaderboard>' + '|'.join(list(dict(settings.LEADERBOARD_CHOICES).keys())) + ')/$', snapshot, name='snapshot'),

	path('avatars/', avatars, name='avatars'),

    re_path(r'^avatars/(?P<avatar>\d{3}.{1,30}.png)/$', select_avatar, name='select_avatar'),

]