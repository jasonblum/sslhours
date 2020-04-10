import random, os, decimal
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone

from faker import Faker
fake = Faker()

from shared.utilities import get_object_or_None
from activities.models import Activity
from organizations.models import Organization
from schools.models import School
from servicehours.models import ServiceHour
from students.models import Student
from teams.models import Team
from features.models import Feature


User = get_user_model()


class Command(BaseCommand):
	help = 'Generates realistic demo data'

	def handle(self, *args, **options):

		os.remove(settings.DATABASES['default']['NAME'])
		print(f'Deleted: {settings.DATABASES["default"]["NAME"]}')

		call_command('migrate')
		print('New database created and migrated')

		User.objects.create_superuser(
			password='zulu',
			email=settings.ADMIN_EMAIL,
		)
		print('admin created')



		for school_type in ['middle', 'high']:
			print(f'Creating {school_type} Schools...')
			filename = f'{os.getcwd()}/shared/management/commands/{school_type}_schools.txt'
			
			with open(filename, 'r') as filehandle:
				for line in filehandle:
					d = {}
					data = line.split('|')

					address_line = data[1].split(',')

					school, _ = School.objects.update_or_create(
						mcps_school_id = int(data[0]),
						defaults = {
							'name' : address_line[0],
							'address' : address_line[1],
							'city' : ' '.join(address_line[2].split()[0:-1]),
							'zip_code' : address_line[2].split()[-1],
							'phone' : data[2],
							'school_type' : school_type,
						}
					)
					school.save()
		print('schools created')

		coordinator = User.objects.create_user(
			email='coordinator@gmail.com',
			password='SSLHours',
		)
		for school in School.objects.all():
			school.ssl_coordinators.add(coordinator)
		print('coordinator created and added to all schools')




		manager = User.objects.create_user(
			email='manager@gmail.com',
			password='SSLHours',
		)

		organization1 = Organization.objects.create(
			name = 'B-CC HS PTSA',
			ein = '52-6070540',
			phone = '(240) 740-0400',
			email = 'volunteerbccbooksale@gmail.com',
			address = '4301 East-West Highway',
			city = 'Bethesda',
			state = 'MD',
			zip_code = '20814',
			description = 'The B-CC 2020 Used Book Sale will take place on Saturday, March 7th from 10 a.m. to 5 p.m. and Sunday March 8th from 10 a.m. to 3 p.m. Your used book donations and precious volunteer time will make the B-CC 2020 Used Book Sale a success.  Please participate!  The funds raised will benefit ALL B-CC students and many school and teacher programs.',
			website = 'https://www.bccptsa.net/used-book-sale',
			manager = manager
		)
		print('organization1 created')

		organization2 = Organization.objects.create(
			name = 'A Wider Circle',
			ein = '52-2345144',
			phone = '(301) 608-3504',
			email = 'contact@awidercircle.org',
			address = '9519 Brookville Road',
			city = 'Silver Spring',
			state = 'MD',
			zip_code = '20910',
			description = 'The mission of A Wider Circle is to end poverty through on-the-ground programs and services, as well as through the development of large-scale solutions to its root causes. Our holistic approach focuses on the creation of stable homes; workforce development programming to move families to economic self-sufficiency; neighborhood revitalization; and the creation of greater awareness and engagement by the community, as a whole.',
			website = 'https://awidercircle.org/',
			manager = manager
		)
		print('organization1 created')

		for i in range(10):
			organization = Organization.objects.create(
				name = fake.company(),
				ein = fake.ein(),
				phone = fake.phone_number(),
				email = fake.email(),
				address = fake.street_address(),
				city = fake.city(),
				state = 'MD',
				zip_code = fake.zipcode_in_state(state_abbr='MD'),
				description = fake.text(),
				website = fake.url(),
				manager = manager
			)			
			print(f'Organization {organization} created...')






		activity1 = Activity.objects.create(
			name = 'Book Sorting',
			description = 'Assist receiving books at drop-off, sorting, general support.',
			organization = organization1,
			manager = manager,
		)
		print('activity1 created')
		activity2 = Activity.objects.create(
			name = 'Receiving',
			description = 'Assist receiving and sorting furniture and clothing at drop-off, sorting, general support.',
			organization = organization2,
			manager = manager,
		)
		print('activity1 created')



		team1 = Team.objects.create(
			name = 'World of Change Club',
			description = 'World Of Change is an organization based in Maine and their goal is to collect loose change (and dollars) to help local organizations with many issues including Housing, Food, Health, Education etc. They have spread their work to many schools around the country, and we are excited to bring it to B-CC. Join us as we fundraise for a great cause!',
			website = 'https://www.worldofchange.world/'
		)
		print('team1 created')
		team2 = Team.objects.create(
			name = 'Robotics Team',
			description = 'The Robotics Team at ABC High School',
			website = 'http://abcrobotics.org/'
		)
		print('team2 created')
		team3 = Team.objects.create(
			name = 'Varsity Girls Soccer',
			description = 'Girls Varsity Soccer at ABC High School',
			website = 'https://abcvarsitysoccer.org'
		)
		print('team3 created')


		bcc = School.objects.get(mcps_school_id=406)
		student1 = Student.objects.create(
			mcps_id = '1234',
			_beginning_total_servicehour_balance = decimal.Decimal(130.5),
			username = 'eso',
			grade = 11,
			first_name ='Eső',
			last_name ='Csíkos',
			school = bcc,
			team = team1,
			first_period_teacher = 'Ms. Mikulski',
			parent_name ='Jason Blum',
			parent_phone ='240-999-9999',
			parent_phone_other ='301-555-5555'
		)
		print('student1 created')

		user1 = User.objects.create_user(
			email='user@gmail.com',
			password = 'SSLHours',
			student = student1
		)
		print('user1 created')

		start_time = fake.date_time_this_month(before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())
		servicehour1 = ServiceHour.objects.create(
			start_time = start_time,
			end_time = start_time + timedelta(minutes=137),
			crediting_SSL_coordinator = coordinator,
			student = student1,
			activity = activity1,
			school = student1.school,
			grade = student1.grade,
			team = student1.team
		)
		print('servicehour1 created')

		start_time = fake.date_time_this_month(before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())
		servicehour2 = ServiceHour.objects.create(
			start_time = start_time,
			end_time = start_time + timedelta(minutes=126),
			crediting_SSL_coordinator = coordinator,
			student = student1,
			activity = activity1,
			school = student1.school,
			grade = student1.grade,
			team = student1.team
		)
		print('servicehour2 created')

		teams = Team.objects.all()
		for school_type in ['middle', 'high']:
			schools = School.objects.filter(school_type=school_type)

			for i in range(40):
				student = Student.objects.create(
					mcps_id = random.randint(99,999999),
					_beginning_total_servicehour_balance = decimal.Decimal(random.randint(1,22)),
					username = fake.profile()['username'],
					grade = random.randint(6,8) if school_type == 'middle' else random.randint(9,12),
					first_name = fake.first_name(),
					last_name = fake.last_name,
					school = random.choice(schools),
					team = random.choice(teams),
					first_period_teacher = fake.name(),
					parent_name = fake.name(),
					parent_phone = fake.phone_number(),
					parent_phone_other = fake.phone_number()
				)
				print(f'student created: {student}')
				user = User.objects.create_user(
					email = fake.email(),
					password = 'SSLHours',
					student = student
				)
				print(f'User created: {user}')


		for i in range(40):
			student = Student.objects.create(
				mcps_id = random.randint(99,999999),
			)
			print(f'Unclaimed student created: {student}')


		students = Student.objects.all()
		schools = School.objects.all()
		activities = Activity.objects.all()
		for i in range(100):
			student = random.choice(students)
			start_time = fake.date_time_this_month(before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())
			co = coordinator if bool(random.getrandbits(1)) else None
			reflections = 'My reflection text...' if co else 'My reflection text...' if bool(random.getrandbits(1)) else None

			servicehour = ServiceHour.objects.create(
				start_time = start_time,
				end_time = start_time + timedelta(minutes=random.randint(15, 130)),
				crediting_SSL_coordinator = co,
				reflections = reflections,
				student = student,
				activity = random.choice(activities),
				school = student.school,
				grade = student.grade,
				team = student.team
			)
			print(f'Servicehour created: {servicehour}')








		feature1 = Feature.objects.create(
			name = 'Login with Gmail',
			discussion = 'Instead of having to remember my password on SSLHours.com, can I just log in with my Gmail account?',
			status = 'completed',
			outcome = 'Done - you can log in with your google account.'
		)
		feature2 = Feature.objects.create(
			name = 'Login with Instagram',
			discussion = 'Instead of having to remember my password on SSLHours.com, can I just log in with my Instagram account?'
		)
		feature3 = Feature.objects.create(
			name = 'Links to share leaderboard position certificates on college applications',
			discussion = 'I\'d like to be able to save a snapshot of my position on one more leaderboards and present it as a "certificate" I can share with colleges.  This certificate should have a short URL an admissions officer can click on to see my standing, review hours I\'ve worked and even read my reflections text...' 
		)
		print('features created')




		self.stdout.write(self.style.SUCCESS('ok all done!'))






