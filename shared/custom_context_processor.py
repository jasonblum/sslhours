from django.conf import settings


def custom_proc(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_SUPPORT_EMAIL': settings.SITE_SUPPORT_EMAIL,
        'GRADE_CHOICES': settings.GRADE_CHOICES,
    }
