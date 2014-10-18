# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, get_list_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

# models and forms
from offre.models import Offer
from article.models import Article
from car_shop.forms import Search_Form, Text_Search_Form
from profile.models import Profile_candid, Profile_emp
from profile.forms import UserInfoForm, EmployerInfoForm
# pagination and search
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from model_choices import REGION_CHOICES, SALARY_CHOICES, CATEGORY_CHOICES, OFFER_CHOICES, YESNO
from django.db.models import F
from django.conf import settings

# login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

from django.core.mail import send_mail
from django.contrib import messages
from django.core.context_processors import csrf
from django.utils import translation

# decorating and caching
from functools import wraps
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from speedjob.settings import CACHE_TIMEOUT

def set_notification_message(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        msg = None
        # msg = None
        if request.user.is_authenticated():
            u = request.user
            if u.groups.filter(name="candidate"):
                profile = Profile_candid.objects.get(user = u)
                msg = profile.get_all_fields()
            elif u.groups.filter(name="employer"):
                profile = Profile_emp.objects.get(user = u)
                msg = profile.get_all_fields()    
        else:
            msg = None
        return view(request, msg, *args, **kwargs)
    return wrapper
    

@set_notification_message
def home(request, msg):
    # offers      = Offer.objects.index_is_activated
    offer_cache_key = request.path+'index'
    offers = cache.get(offer_cache_key)
    if not offers:
        offers = Offer.objects.filter(activated = True).order_by('-created')[:8]
        cache.set(offer_cache_key, offers, CACHE_TIMEOUT)

    form        = Search_Form()
    text_form   = Text_Search_Form()
    articles    = Article.objects.all()[:4]
    
    return render_to_response('index.html', locals(), context_instance = RequestContext(request))
    
def search(request):
    # preparing forms
    text_form   = Text_Search_Form()
    form        = Search_Form()

    # preparing search words if we came from the index page
    offer       = request.GET.get('offer')
    category    = request.GET.get('category')
    region      = request.GET.get('region')
    low_salary  = request.GET.get('low_salary')
    high_salary = request.GET.get('high_salary')
    page        = request.GET.get('page')

    # in the normal display of the view
    if region == None : region = 'all'
    if category == None : category = 'all'
    if offer == None : offer = 'all'
    if low_salary == None : low_salary = 'all'
    if high_salary == None : high_salary = 'all'

    offers          = Offer.objects.all().filter(activated=True)
    
    if region       != "all":   offers = offers.filter(region   = region)
    if category     != 'all':   offers = offers.filter(category = category)
    if offer        != 'all':   offers = offers.filter(offerType    = offer)
    if low_salary   != 'all':   offers = offers.filter(salary__gte=int( low_salary ))
    if high_salary  != 'all':   offers = offers.filter(salary__lte= int( high_salary ))

    articles    = offers
    paginator   = Paginator(articles, 8) 
    page        = request.GET.get('page')
    query        = request.GET.get('region')

    try: contacts = paginator.page(page)
    except PageNotAnInteger: contacts = paginator.page(1)
    except EmptyPage: contacts = paginator.page(paginator.num_pages)

    return render_to_response('search.html' , locals(), context_instance = RequestContext(request))

def map_search(request):
    # preparing forms
    text_form   = Text_Search_Form()
    form        = Search_Form()

    # preparing search words if we came from the index page
    offer       = request.GET.get('offer')
    category    = request.GET.get('category')
    region      = request.GET.get('region')
    low_salary  = request.GET.get('low_salary')
    high_salary = request.GET.get('high_salary')
    page        = request.GET.get('page')

    # in the normal display of the view
    if region == None : region = 'all'
    if category == None : category = 'all'
    if offer == None : offer = 'all'
    if low_salary == None : low_salary = 'all'
    if high_salary == None : high_salary = 'all'

    offers          = Offer.objects.all().filter(activated=True)

    if region       != "all":   offers = offers.filter(region   = region)
    if category     != 'all':   offers = offers.filter(category = category)
    if offer        != 'all':   offers = offers.filter(offerType    = offer)
    if low_salary   != 'all':   offers = offers.filter(salary__gte=int( low_salary ))
    if high_salary  != 'all':   offers = offers.filter(salary__lte= int( high_salary ))

    articles  = offers
    paginator = Paginator(articles, 8) 
    page      = request.GET.get('page')
    query     = request.GET.get('region')

    try: contacts = paginator.page(page)
    except PageNotAnInteger:    contacts = paginator.page(1)
    except EmptyPage:           contacts = paginator.page(paginator.num_pages)

    return render_to_response('map_search.html', locals(), context_instance = RequestContext(request))

def get_pagination_page(page=1, items=None):

    items = Offer.objects.all().filter(activated=True)
    paginator = Paginator(items, 4)
    try: page = int(page)
    except ValueError: page = 1

    try:    items = paginator.page(page)
    except  (EmptyPage, InvalidPage): items = paginator.page(paginator.num_pages)

    return items

def land_page_pagination(page=1, items=None):
    # items = range(0, 100)
    items = items
    paginator = Paginator(items, 8)
    
    try:    page = int(page)
    except  ValueError: page = 1

    try:    items = paginator.page(page)
    except  (EmptyPage, InvalidPage): items = paginator.page(paginator.num_pages)

    return items


def contact(request):
    errors = []
    if request.method == 'POST':
        print 'in POST'

        if not request.POST.get('name', ''): errors.append('Enter a name')
        if not request.POST.get('subject', ''): errors.append('Enter a subject.')
        if not request.POST.get('message', ''): errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']: errors.append('Enter a valid e-mail address.')
        # create a model to just save contact messages tickets  
        if not errors:
            print 'sending message'
            try:
                send_mail(
                    #subject
                    request.POST['subject'],
                    #message
                    request.POST['message'],
                    # from
                    request.POST.get('email'),
                    # To [recipient list]
                    ['redatest7@gmail.com'],
                )
                messages.add_message(request, messages.INFO, 'message sent successflully.')
                # return render_to_response('contact.html', locals(), context_instance = RequestContext(request))
                return HttpResponseRedirect('/contact')
            except Exception, err:
                messages.add_message(request, messages.INFO, 'there was an error when processing your request.')
                return render_to_response('contact.html', locals(), context_instance = RequestContext(request))
            
    return render_to_response('contact.html', locals(), context_instance = RequestContext(request))

