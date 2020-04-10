from django.test import TestCase
from django.urls import reverse, resolve

from sslhours.views import home


class HomepageTests(TestCase):
	def setUp(self):
		url = reverse('home')
		self.response = self.client.get(url)

	def test_homepage_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_homepage_template(self):
		self.assertTemplateUsed(self.response, 'home.html')

	def test_homepage_contains_correct_html(self):
		self.assertContains(self.response, 'Welcome to ')

	def test_homepage_does_not_contain_incorrect_html(self):
		self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

	def test_homepage_url_resolves_home(self):
		view = resolve('/')
		self.assertEqual(view.func.__name__, home.__name__)