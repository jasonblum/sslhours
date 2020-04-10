from django.contrib import admin


from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ('name', 'school_type', 'mcps_school_id', 'city', 'zip_code', 'phone', 'ssl_coordinators_names_hyperlinked', 'is_active', )
	search_fields = ('name', 'mcps_school_id', 'city', 'zip_code', 'phone', )

	def get_actions(self, request):
		actions = super().get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions