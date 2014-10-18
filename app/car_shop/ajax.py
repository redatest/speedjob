from django.utils 				import simplejson
from dajaxice.decorators 		import dajaxice_register
from dajaxice.utils 			import deserialize_form
from dajax.core 				import Dajax
from car_shop.forms 			import Search_Form, Text_Search_Form
from offre.models	 			import Offer
# pagination example
from car_shop.views 			import get_pagination_page, land_page_pagination
from django.template.loader 	import render_to_string
from car_shop.model_choices 	import REGION_CHOICES, SALARY_CHOICES, CATEGORY_CHOICES, OFFER_CHOICES, YESNO

from django.core.paginator 		import Paginator
from django.utils 				import simplejson as json
import urllib2
from django.http import HttpResponseRedirect

# field based search
def make_query(form):
	form = form
	# print form

	print form.errors
	cars 			= Offer.objects.all()
	print cars
	frm_region 		= (form.cleaned_data.get('region'))
	frm_category 	= form.cleaned_data.get('category')
	frm_offer 		= form.cleaned_data.get('offer')
	frm_low_salary 	= form.cleaned_data.get('low_salary')
	frm_high_salary = form.cleaned_data.get('high_salary')

	# print "frm_high_salary"
	print frm_high_salary ,frm_low_salary, frm_category, frm_region, frm_offer

	if frm_region 		!= 'all': 	cars = cars.filter(region 	= frm_region)
	if frm_category 	!= 'all': 	cars = cars.filter(category = frm_category)
	if frm_offer 		!= 'all': 	cars = cars.filter(offer 	= frm_offer)

	if frm_low_salary 	!= 'all': 	cars = cars.filter(salary__gte=int(frm_low_salary))
	if frm_high_salary 	!= 'all': 	cars = cars.filter(salary__lte= int(frm_high_salary))
		
	return cars			

@dajaxice_register
def sayhello(request):
	return simplejson.dumps({'message':'Hello World'})

@dajaxice_register
def send_form(request, form):
	print 'in send form'
	dajax = Dajax()
	form = Search_Form(deserialize_form(form))

	print 'errors'
	print form.errors
	
	# must do this to clean the form
	if form.is_valid():

		print 	'form is valid'
		cars 	= make_query(form)
		items 	= land_page_pagination(page=1, items=cars)
		render 	= render_to_string('./parts/pagination_page2.html', {'items': items})

		
		dajax 	= Dajax()

		dajax.assign('#respo', 'innerHTML', render)
		# print(dir(dajax.json()))
		return dajax.json()

	else:
		dajax.alert('error in form validation')

	return dajax.json()

@dajaxice_register
def pagination2(request, p, form):
	print 'in pagination 2'
	form = Search_Form(deserialize_form(form))
	
	if form.is_valid():
		cars 	= make_query(form)
		items 	= land_page_pagination(page=p, items=cars)
		render 	= render_to_string('./parts/pagination_page2.html', {'items': items})
		dajax 	= Dajax()
		dajax.assign('#respo', 'innerHTML', render)

		return dajax.json()

	else:
		dajax.alert('error in form validation')

	return dajax.json()
# textual search
import re

from django.db.models import Q

def normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):
	''' Splits the query string in invidual keywords, getting rid of unecessary spaces
		and grouping quoted words together.
		Example:

		>>> normalize_query('  some random  words "with   quotes  " and   spaces')
		['some', 'random', 'words', 'with quotes', 'and', 'spaces']

	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
	''' Returns a query, that is a combination of Q objects. That combination
		aims to search keywords within a model by testing the given search fields.

	'''
	query = None # Query to search for every search term
	terms = normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query


@dajaxice_register
def text_send_form(request, form):
	print 'in text send form'
	query_string 	= ''
	found_entries 	= None
	dajax 			= Dajax()
	form 			= Text_Search_Form(deserialize_form(form))

	print 'errors'
	print form.errors
	
	# must do this to clean the form
	if form.is_valid():
		print 'form is valid'
		text 			= form.cleaned_data['target_text']
		query_string 	= text
		entry_query 	= get_query(query_string, ['title', 'category',])
		print entry_query
		found_entries 	= Offer.objects.filter(entry_query)
		items 			= land_page_pagination(page=1, items=found_entries)
		render 			= render_to_string('./parts/pagination_page2.html', {'items': items})
		dajax 			= Dajax()
		dajax.assign('#respo', 'innerHTML', render)
		return dajax.json()

	else:
		dajax.alert('error in form validation')

	return dajax.json()
