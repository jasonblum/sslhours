from django.urls import path, re_path


from .views import list_features, vote


app_name = 'features'

urlpatterns = [

	path('', list_features, name='list'),
    re_path(r'^(?P<upordown>(up|down))/(?P<pk>[0-9]+)/$', vote, name='vote'),
 
]


