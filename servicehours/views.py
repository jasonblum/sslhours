from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils import timezone

from stronghold.views import public
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from shared.utilities import get_object_or_None

from .models import ServiceHour
from .forms import ServiceHourForm, CommentForm



def edit(request, pk):
	servicehour = get_object_or_None(ServiceHour, pk=pk)
	servicehour_form = ServiceHourForm(request.POST or None, instance=servicehour)

	credit = 'credit' in request.POST or False

	comment_form = CommentForm(request.POST)
	if request.POST and servicehour_form.is_valid():

		servicehour = servicehour_form.save()
		servicehour.school = servicehour.student.school
		servicehour.grade = servicehour.student.grade
		if credit:
			servicehour.crediting_SSL_coordinator = request.user
		servicehour.save()

		if comment_form.is_valid() and len(comment_form.cleaned_data.get('comment')):
			comment = comment_form.save(commit=False)
			comment.servicehour = servicehour
			comment.author = request.user
			comment.save()
		messages.success(request, f'{servicehour} has been saved.')
		return redirect('servicehours:detail', pk=pk)

	return render(request, 'servicehours/edit.html', 
		{
		'servicehour_form': servicehour_form, 
		'servicehour': servicehour, 
		'comment_form': comment_form, 
		'can_credit': request.user in servicehour.users_who_can_credit
		}
	)


@public
def list_servicehours(request):
	servicehours = ServiceHour.objects.select_related(
		'activity', 'activity__organization', 'student', 'student__user', 'team', 'school',
		).prefetch_related(
		'school__ssl_coordinators'
		)
	return render(request, 'servicehours/list.html', {'servicehours':servicehours})


def detail(request, pk):
	servicehour = get_object_or_404(ServiceHour, pk=pk)
	return render(request, 'servicehours/detail.html', {'servicehour':servicehour})



def pdf(request, pk):
	servicehour = get_object_or_404(ServiceHour, pk=pk)

	packet = BytesIO()
	# create a new PDF with Reportlab
	p = canvas.Canvas(packet, pagesize=letter)

	p.drawString(170, 559, f'{servicehour.student.last_name}, {servicehour.student.first_name}')
	p.drawString(485, 559, f'{servicehour.student.mcps_id}')
	p.drawString(558, 559, f'{servicehour.student.grade}')

	p.drawString(58, 544, f'{servicehour.student.school}')
	p.drawString(380, 544, f'{servicehour.student.first_period_teacher}')

	p.drawString(58, 530, f'{servicehour.student.user.email}')

	p.drawString(125, 515, f'{servicehour.student.parent_name}')
	p.drawString(393, 515, f'{servicehour.student.parent_phone}')
	p.drawString(501, 515, f'{servicehour.student.parent_phone_other}')

	p.drawString(83, 466, f'{servicehour.activity.organization}')
	p.drawString(360, 466, f'{servicehour.activity.organization.ein}')
	p.drawString(500, 466, f'{servicehour.activity.organization.phone}')

	p.drawString(70, 451, f'{servicehour.activity.organization.address}')
	p.drawString(391, 451, f'{servicehour.activity.organization.email}')

	p.drawString(146, 436, f'{servicehour.activity.description}')

	p.drawString(40, 369, f'{servicehour.start_time.strftime("%m/%d/%y, %-I:%M %p")}')
	p.drawString(188, 369, f'{servicehour.end_time.strftime("%m/%d/%y, %-I:%M %p")}')
	p.drawString(350, 369, '1')
	p.drawString(411, 369, f'{servicehour.total}')
	p.drawString(511, 369, f'{servicehour.total}')

	p.drawString(131, 354, f'{servicehour.activity.manager}')

	p.drawString(515, 341, f'{timezone.now().strftime("%m/%d/%y")}')

	p.drawString(28, 211, f'{servicehour.reflections}')

	p.drawString(433, 78, f'Credited on SSLHours.com?')
	p.drawString(478, 61, f'ID #{servicehour.pk} [_]')


	p.save()

	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	# read your existing PDF
	existing_pdf = PdfFileReader(open(settings.SSL_PDF, "rb"))
	output = PdfFileWriter()
	# add the "watermark" (which is the new pdf) on the existing page
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)



	# finally, write "output" to a byte stream
	outputStream = BytesIO()
	output.write(outputStream)

	response = HttpResponse(content_type="application/pdf")
	response['Content-Disposition'] = f'attachment; filename={servicehour.student.mcps_id}_{pk}_560-51.pdf'
	response.write(outputStream.getvalue())
	return response