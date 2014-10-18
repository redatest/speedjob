from django.conf import settings
# from ourforum.models import Offer
from django.utils.translation import ugettext_lazy as _
# from car_shop.forms import CustomRegistrationForm

def strings(request):
	""" context processor for the site templates """
	if request.LANGUAGE_CODE == "en":
		direction = "ltr"
	else:
		direction = "rtl"

	return {
			'request': request,
			'direction' : direction
			# 'register_form': CustomRegistrationForm

			}

