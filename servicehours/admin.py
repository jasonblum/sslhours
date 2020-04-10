from django.contrib import admin


from .models import ServiceHour



@admin.register(ServiceHour)
class HourAdmin(admin.ModelAdmin):
	list_display = ('student', 'start_time', 'end_time', 'total', 'grade', 'team', 'school', 'crediting_SSL_coordinator', 'status', )
	search_fields = ('student', 'crediting_SSL_coordinator', 'status', )

	def get_actions(self, request):
		actions = super().get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions