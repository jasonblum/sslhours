'''
REMEMBER python manage.py check --deploy
REMEMBER python manage.py check --deploy
REMEMBER python manage.py check --deploy
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
?: (security.W018) You should not have DEBUG set to True in deployment.
?: (security.W020) ALLOWED_HOSTS must not be empty in deployment.
?: (security.W022) You have not set the SECURE_REFERRER_POLICY setting. Without this, your site will not send a Referrer-Policy header. You should consider enabling this header to protect user privacy.
'''



import os, sys, environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
ENVIRONMENT = env('ENVIRONMENT')
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')



SITE_ID = 1


ALLOWED_HOSTS = ['127.0.0.1', 'sslhours.com', 'www.sslhours.com', ]

SITE_NAME = 'SSLHours'
SITE_SUPPORT_EMAIL = 'help@sslhours.com'

#Version numbering follows PEP386 ABC pattern: ‘A’ = Major release breaking backwards compatibility, 'B' = features, 'C' = bug fixes.
VERSION = '0.1.0'


# Application definition

INSTALLED_APPS = [
    #DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #THIRD PARTY
    'impersonate',
    'sekizai',
    'stronghold',
    'crispy_forms',
    'anymail',
    'mail_templated',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    #allauth social providers
    'allauth.socialaccount.providers.google',

    #APPLICATION APPS
    'users.apps.UsersConfig',
    'schools.apps.SchoolsConfig',
    'students.apps.StudentsConfig',
    'servicehours.apps.ServicehoursConfig',
    'organizations.apps.OrganizationsConfig',
    'activities.apps.ActivitiesConfig',
    'shared.apps.SharedConfig',
    'teams.apps.TeamsConfig',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ANYMAIL = {
    "SENDINBLUE_API_KEY": env('SENDINBLUE_API_KEY'),
}
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
DEFAULT_FROM_EMAIL = SITE_SUPPORT_EMAIL
SERVER_EMAIL = SITE_SUPPORT_EMAIL

AUTH_USER_MODEL = 'users.User'


AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    # For each OAuth based provider, either add a ``SocialApp``
    # (``socialaccount`` app) containing the required client
    # credentials, or list them here:
    'google': {
        'APP': {
            'client_id': env('SOCIALACCOUNT_PROVIDERS_GOOGLE_CLIENTID'),
            'secret': env('SOCIALACCOUNT_PROVIDERS_GOOGLE_SECRET'),
        }
    },
}
SOCIALACCOUNT_AUTO_SIGNUP = True

# https://medium.com/@royprins/django-custom-user-model-email-authentication-d3e89d36210f
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'shared.custom_middleware.SSLHoursMiddleware',

    'impersonate.middleware.ImpersonateMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'sslhours.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'shared/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'shared.custom_context_processor.custom_proc',
            ],
        },
    },
]

WSGI_APPLICATION = 'sslhours.wsgi.application'




# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sslhours.db.sqlite3'),
    }

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'sslhours',
    #     'USER': 'sslhours',
    #     'PASSWORD': 'gavagai',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # }

}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
    ('hu', _('Hungarian')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'shared/static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder", 
]


ADMIN_URL = env('ADMIN_URL')
ADMIN_EMAIL = env('ADMIN_EMAIL')
ADMINS = (
    ('admin', ADMIN_EMAIL),
)

# DEBUG TOOLBAR
if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
        'rosetta',
    )

    #Django Debug Toolbar Configuration
    #URL:  https://github.com/django-debug-toolbar/django-debug-toolbar
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
        'INTERCEPT_REDIRECTS': False
    }



# DJANGO-IMPERSONATE
IMPERSONATE_REDIRECT_URL = '/'
IMPERSONATE_URI_EXCLUSIONS = [f'^/{ ADMIN_URL }.+$', ]
IMPERSONATE_REQUIRE_SUPERUSER = True
IMPERSONATE_ALLOW_SUPERUSER = True


# DJANGO-STRONGHOLD
STRONGHOLD_DEFAULTS = True
STRONGHOLD_PUBLIC_URLS = (
    r'^/__debug__/.+$',
    r'^/i18n/setlang/?$',
)
STRONGHOLD_PUBLIC_NAMED_URLS = (
    'account_login',
    'account_signup',
    'google_login',
    'google_callback',
    'video',
)


if not DEBUG:
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        send_default_pii=True
    )



#APPLICATION STUFF
SSL_PDF = os.path.join(BASE_DIR, '560-51.pdf')
URL_TO_OFFICIAL_SSL_PDF = 'https://www.montgomeryschoolsmd.org/departments/forms/pdf/560-51.pdf'

AVATARS = [png for png in os.listdir(os.path.join(BASE_DIR, 'shared/static/shared/images/avatars')) if png.endswith('.png')]

GRADE_CHOICES = (
    (6, 'Sixth'),
    (7, 'Seventh'),
    (8, 'Eighth'),
    (9, 'Ninth'),
    (10, 'Tenth'),
    (11, 'Eleventh'),
    (12, 'Twelth'),
)

SCHOOL_TYPE_CHOICES = (
    ('middle', 'Middle'),
    ('high', 'High'),
)

LEADERBOARD_CHOICES = (
    ('students', 'Students'),
    ('middle_schools', 'Middle Schools'),
    ('high_schools', 'High Schools'),
    ('teams', 'Teams'),
    ('activities', 'Activities'),
    ('organizations', 'Organizations'),
)

DEFAULT_SERVICE_HOUR_REFLECTION_TEXT = '''
• What did you do?
• What need did your service address?
• Who benefitted from your service?
• What did you learn about yourself?
• How was this experience connected to something you learned in a class at school? (For example, English, Mathematics, Science, Social Studies, Arts,
Physical Education, Health, Foreign Language, etc.)
Note: This reflection will be reviewed by the MCPS SSL coordinator and returned to the student if not complete. '''

