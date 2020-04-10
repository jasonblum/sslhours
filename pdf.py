import os
import pdfrw


INVOICE_TEMPLATE_PATH = '/Users/jasonblum/Desktop/sslhours/560-51.pdf'
INVOICE_OUTPUT_PATH = '/Users/jasonblum/Desktop/sslhours/560-51-OUT.pdf'



template_pdf = pdfrw.PdfReader(INVOICE_TEMPLATE_PATH)

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'


data = {
  '(student)': 'Smith, John Jacob Jingleheimer',
  '(id)': '123456',
  '(grade)': 10,
  '(school)': 'Silver Creek MS - 101',
  '(ein)': '99-9999999',
  '(teacher)': 'Ms. Doolittle',
  '(email)': 'zanzibar@yahoo.com',
  '(parent)': 'Englebert Humperdink',
  '(phone)': '555-555-5555',
  '(other_phone)': '555-555-5555',
  '(organization)': 'Organization One, LLC',
  '(ein)': '55-5555555',
  '(org_phone)': '555-555-5555',
  '(org_address)': '1 Main Street; Bethesda, MD  20815',
  '(org_email)': 'asdfasdf@asdfasdf.com',
  '(activity)': 'asdf asdf asdf asdf asdf',
  '(date_from)': '12/12/20',
  '(date_to)': '12/12/20',
  '(number_days)': '99',
  '(number_per_day)': '24',
  '(total)': '99',
  '(supervisor)': 'Jeremiah Bullfrog',
  '(supervisor_title)': 'Director, Hasselback Industries',
  '(supervisor_signature)': 'Jeremiah Bullfrog',
  '(supervisor_date)': '12/12/20',
  '(reflections)': '''
    I enjoyed this experience because I blah blah blah blah blah blah blah blah blah blah blah blah blah blah 
    blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah 
    blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah end
  ''',
  '(date)': '12/12/20',
  '(sslhours)': 'Please confirm these hours on http://SSLHours.com',
}


annotations = template_pdf.pages[0]['/Annots']

cioteam


for annotation in annotations:
  if annotation['/Subtype'] == '/Widget' and annotation['/T']:
    key = annotation['/T']
    if key in data.keys():
      annotation.update(
        pdfrw.PdfDict(V=f'{data[key]}')
      )


pdfrw.PdfWriter().write(INVOICE_OUTPUT_PATH, template_pdf)
