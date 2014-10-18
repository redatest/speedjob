# -*- coding: utf-8 -*-
from django.contrib import admin
from offre.models import Offer

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


# add image display to car administration
class AdminImageWidget(AdminFileWidget):
	def render(self, name, value, attrs=None):
		output = []
		if value and getattr(value, "url", None):
			image_url = value.url
			file_name=str(value)
			output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="80" height="80" /></a> <br/> %s ' % \
				(image_url, image_url, file_name, _('Change:')))
		output.append(super(AdminFileWidget, self).render(name, value, attrs))
		return mark_safe(u''.join(output))

class OfferAdmin(admin.ModelAdmin):
	list_display 	= ('title','offerType', 'region', 'offerType', 'salary', 'user')
	# delete selected car and it's  file
	
admin.site.register(Offer, OfferAdmin)
