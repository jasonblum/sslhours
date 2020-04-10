from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		exclude = ('is_active', 'mcps_id', 'avatar', )



class ClaimMCPSIDForm(forms.Form):
	mcps_id = forms.IntegerField(initial='123456', min_value=0, max_value=99999999)
	mcps_id_2 = forms.IntegerField(initial='123456', min_value=0, max_value=99999999)
	parent_signature = forms.CharField()

	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data.get("mcps_id") != cleaned_data.get("mcps_id_2"):
			raise forms.ValidationError('Please make sure your MCPS ID is correct.')