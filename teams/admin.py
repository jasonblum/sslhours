from django.contrib import admin


from .models import Team



@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'total_servicehours', 'is_active', )

