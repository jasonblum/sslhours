from django.conf import settings


HELP_TEXT = {

	'What is this?!':
	'''
	


	SSLHours.com aspires to replace this form: <a href="https://www.montgomeryschoolsmd.org/departments/forms/pdf/560-51.pdf">https://www.montgomeryschoolsmd.org/departments/forms/pdf/560-51.pdf</a>
	''',
	
	'Privacy Policy?':
	'''<p>If you just want the SSL Activity and organization printed on the SSL form, then you don't have to share anything with SSLHours.</p>
		<p>If you want the form filled out with everything needed to submit it to your SSL Coordinator - or if you want to skip the form altogether, and just have your SSL Coordinator log in and see your hours, then you have to share your:</p>
	<ul>
		<li>Student MCPS ID</li>
		<li>First and last name</li>
		<li>Grade</li>
		<li>School</li>
		<li>E-mail</li>
	</ul>

	<p>This information is then shared <strong>only</strong> with the student's school's official school SSL Coordinators.</p>

	<p>All other users and the public see <strong>only</strong> the student's username and the service hours they have been credited.</p>
	''',

	'How do I know whether an activity or organization has been approved?':
	f'For now, it is the students responibility to follow existing guidelines on <a href="https://www.montgomeryschoolsmd.org/departments/ssl/">https://www.montgomeryschoolsmd.org/departments/ssl/</a>.',

	'How do I know when I have been credited SSL Hours?':
	f'Check <a href="https://www.montgomeryschoolsmd.org/uploadedFiles/departments/ssl/How%20to%20Check%20Student%20Service%20Learning%20Hours%20on%20MyMCPS%20Portal.pdf">MyMCPS</a>.  You should also receive an email when your school\'s SSL Coordinator has verified and credited your hours here.',

	'How do I create or manage an organization?':
	f'For now, please email <a href="{settings.SITE_SUPPORT_EMAIL}">{settings.SITE_SUPPORT_EMAIL}</a>',

	'How do I create or manage an SSL event or activity?':
	f'For now, please email <a href="{settings.SITE_SUPPORT_EMAIL}">{settings.SITE_SUPPORT_EMAIL}</a>',

	'What are Teams and how do I create one?':
	f'Teams allow students to associate specific SSL Hours with a Team, like "Einstein Robotics" or "Girls Who Code @ B-CC".  To add a team, for now, please email <a href="{settings.SITE_SUPPORT_EMAIL}">{settings.SITE_SUPPORT_EMAIL}</a>',

	'Why do some schools not seem to have as many service hours as their students?':
	f'SSL Coordinators can credit students with a starting balance of service hours, but the system can\'t determine which schools they attended when they completed those hours.  Schools\' balances can only reflect service hours credited on  {settings.SITE_NAME}.',

	'Who and how was this application built?':
	f'''
	This application was built by a couple of parents of MCPS students who found the old SSL form-based process a little tedious and decided to streamline it in a side-project intended also to show off their programming chops.
	The app stores no sensitive data and is completely free and open sourced.
	It is built on <a href="https://www.python.org/">Python</a>, <a href="https://www.djangoproject.com/">Django</a>, <a href="https://getbootstrap.com/">Bootstrap</a> and <a href="https://jquery.com/">jQuery</a> and hosted on <a href="https://www.pythonanywhere.com/">PythonAnywhere</>''',
}