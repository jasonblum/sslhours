from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from students.models import Student
from servicehours.models import ServiceHour


class UserManager(BaseUserManager):
	# https://medium.com/@royprins/django-custom-user-model-email-authentication-d3e89d36210f

	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		if not email:
			raise ValueError('Users must have an email address')
		email = self.normalize_email(email)
		user = self.model(
			email=email,
			is_staff=is_staff, 
			is_active=True,
			is_superuser=is_superuser, 
			last_login=timezone.now(),
			date_joined=timezone.now(), 
			**extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		user=self._create_user(email, password, True, True, **extra_fields)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=254, unique=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	last_login = models.DateTimeField(null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)

	student = models.OneToOneField(Student, null=True, blank=True, on_delete=models.PROTECT, related_name='user')

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	def delete(self):
		raise ValidationError('Data cannot be deleted, only set is_active=True')

	@property
	def username(self):
		return getattr(getattr(self, 'student', None), 'username', self.email)

	def get_absolute_url(self):
		return reverse('users:detail', args=[self.pk])

	@property
	def hyperlinked_name(self):
		return mark_safe(f'<a href="{self.get_absolute_url()}">{self}</a>')

	@property
	def impersonate(self):
		return mark_safe(f'<a href="/impersonate/{self.pk}">impersonate</a>')

	@property
	def coordinated_servicehours(self):
		return ServiceHour.objects.filter(school__in=self.ssl_coordinated_schools.all())