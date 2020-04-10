from django.contrib import admin


from .models import Student, Snapshot



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('mcps_id', 'user', 'total_servicehours', 'grade', 'school', 'team', 'is_active', )

@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
	list_display = ('dt_created', 'student', 'position', 'out_of', 'leaderboard', )

