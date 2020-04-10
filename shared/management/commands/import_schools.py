import os
from django.core.management.base import BaseCommand, CommandError

from schools.models import School



class Command(BaseCommand):
	help = 'Imports schools'

	def handle(self, *args, **options):


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
							'zip' : address_line[2].split()[-1],
							'phone' : data[2],
							'school_type' : school_type
						}
					)

					print(school.__dict__)

					school.save()


		self.stdout.write(self.style.SUCCESS('ok all done!'))
