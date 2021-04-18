from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views import home, help, trigger_error
from students.views import student_cv



urlpatterns = [

    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('impersonate/', include('impersonate.urls')),

	path('', include('users.urls')),
	path('users/', include('django.contrib.auth.urls')),
	path('accounts/', include('allauth.urls')),

	path('', home, name='home'),
	path('help/', help, name='help'),
    path('privacy/', TemplateView.as_view(template_name="privacy.html"), name='privacy'),

	path('students/', include('students.urls')),
	path('cv/<slug:slug>/', student_cv, name='student_cv'),

	path('organizations/', include('organizations.urls')),
	path('schools/', include('schools.urls')),
	path('activities/', include('activities.urls')),
	path('servicehours/', include('servicehours.urls')),
	path('teams/', include('teams.urls')),

	path('rosetta/', include('rosetta.urls')),
	path('i18n/', include('django.conf.urls.i18n')),

    path('video/', RedirectView.as_view(url='https://www.dropbox.com/s/9y1yrffrjq7s3yz/SSLHours.mov'), name='video'),
	
	path('sentry-debug/', trigger_error),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


handler400 = 'shared.views.handler400'
handler403 = 'shared.views.handler403'
handler404 = 'shared.views.handler404'
handler500 = 'shared.views.handler500'

admin.site.site_header = f'{settings.SITE_NAME}'
admin.site.site_title = f'{settings.SITE_NAME}'
admin.site.index_title = f'{settings.SITE_NAME} Administration Page'
admin.site.unregister(Group)



