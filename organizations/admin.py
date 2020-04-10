from django.contrib import admin


from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('name', 'total_servicehours', 'ein', 'phone', 'email', 'manager', 'is_active', )
	search_fields = ('name', 'ein', 'phone', 'email', 'description', )


	def get_actions(self, request):
		actions = super().get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions
