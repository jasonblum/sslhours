from django.contrib import admin


from .models import Feature, Vote


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
	list_display = ('name', 'tally', 'status', 'outcome', )
	search_fields = ('name', )

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
	list_display = ('feature', 'user', 'upordown', )
	search_fields = ('feature', 'user', )

