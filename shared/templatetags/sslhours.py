from django import template
from django.utils.safestring import mark_safe


register = template.Library()



@register.filter
def status_html(status):
	if status == 'credited':
		html = '<i class="far fa-grin-tongue-wink fa-2x text-success" style="vertical-align: middle;"></i> credited'
	elif status == 'pending':
		html = '<i class="far fa-meh-rolling-eyes fa-2x text-warning" style="vertical-align: middle;"></i> pending'
	else:
		html = '<i class="far fa-sad-cry fa-2x text-dark" style="vertical-align: middle;"></i> incomplete'
	return mark_safe(html)


@register.filter
def datetime(datetime):
	return mark_safe(datetime.strftime("%-m/%d/%y %-I:%M %p")) if datetime else None


@register.filter
def leaderboard_position_html(position):
	if position == 1:
		html = '<i class="fas fa-crown text-warning"></i>'
	elif position == 2:
		html = '<i class="fas fa-award text-dark"></i>'
	elif position == 3:
		html = '<i class="fas fa-award text-muted"></i>'
	else:
		html = ''
	return mark_safe(html)


@register.filter
def keyvalue(dict, key):
    return dict.get(key)

