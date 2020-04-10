from django.contrib import admin


from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
	list_display = ('name', 'total_servicehours', 'description', 'organization', 'managers_names_hyperlinked', 'is_active', )
	search_fields = ('name', 'description', 'organization', )

	def get_actions(self, request):
		actions = super().get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions
