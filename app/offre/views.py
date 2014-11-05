# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
import os

# models and forms
from offre.models import Offer
from offre.forms import OfferForm, EditOfferForm
from profile.models import Profile_candid, Profile_emp, Application
from profile.forms import UserInfoForm, EmployerInfoForm
# pagination and search
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from car_shop.model_choices import REGION_CHOICES, SALARY_CHOICES, CATEGORY_CHOICES, OFFER_CHOICES, YESNO
from django.db.models import F

# login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

from django.core.mail import send_mail
from django.contrib import messages
from django.core.context_processors import csrf
from django.utils import translation

#email
from car_shop.nicemails import send_nice_email
from django.conf import settings
from django.contrib.sites.models import Site

# decorating and caching
from functools import wraps
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from speedjob.settings import CACHE_TIMEOUT


def offer(request, num):
    
    offer_cache_key = request.path
    offer           = cache.get(offer_cache_key)
    if not offer:
        offer = Offer.objects.get(id=num)
        cache.set(offer_cache_key, offer, CACHE_TIMEOUT)

    next        = offer.get_absolute_url()
    offer.views = int(offer.views)+1
    offer.save()

    can_edit        = False
    already_applyed = False

    if request.user.username == offer.user.username: can_edit = True

    # refactor that cause it is ugly
    if request.user.is_authenticated:
        gr = Group.objects.get(name='candidate')
        if request.user in gr.user_set.all():
            sender  = request.user
            applyer = sender.profile_candid_set.latest('id')
            already_applied = applyer in offer.profile_candid_set.all()
            print 'the user %s has already applied to this offer' %sender
            print already_applyed    

    return render_to_response('offre/offer.html', locals(), context_instance = RequestContext(request))

def offer_edit(request, num):
    car = Offer.objects.get(id = num)

    # if request.user.username == car.user.user.username:
    if request.user.username == car.user.username:
        can_edit = True

    if request.method == 'POST':
        form = EditOfferForm(request.POST, request.FILES)

        if form.is_valid():
            changed_fields = form.changed_data

            if 'title' in changed_fields:           title = form.cleaned_data['title']
            if 'category' in changed_fields:        category = form.cleaned_data['category']
            if 'offer' in changed_fields:           offer = form.cleaned_data['offer']
            if 'region' in changed_fields:          region = form.cleaned_data['region']
            if 'salary' in changed_fields:          salary = int(form.cleaned_data['salary'])
            if 'immediate' in changed_fields:       immediate = form.cleaned_data['immediate']
            if 'description' in changed_fields:     description = form.cleaned_data['description']
            if 'expired' in changed_fields:         expired = form.cleaned_data['expired']
                
            else:
                image = car.image       
            
            car.title       = title 
            car.offerType   = offer
            car.salary      = salary
            car.region      = region
            car.category    = category 
            car.immediate   = immediate
            car.description = description
            car.expired     = expired

            car.save()  
            return HttpResponseRedirect(car.get_absolute_url())
            
        else:
            print form.errors   

    else:
        form = EditOfferForm(initial={  'title':        car.title,
                                        'category':     car.category,
                                        'salary':       car.salary,
                                        'region':       car.region,
                                        'offer':        car.offerType,
                                        'immediate':    car.immediate,
                                        'description':  car.description,
                                        'expired':      car.expired
                                        })

    return render_to_response('offre/offer_edit.html', locals(), context_instance = RequestContext(request))

# make the call by ajax
@login_required
def offer_disable(request, num):
    offer = get_object_or_404(Offer, id=num)
    offer.activated = False
    offer.save()
    return HttpResponseRedirect('/emp_profile_offres/')

# todo make the call by ajax
@login_required
def offer_activate(request, num):
    offer = get_object_or_404(Offer, id=num)
    offer.activated = True
    offer.save()
    return HttpResponseRedirect("/emp_profile_offres/")

# @login_required
def offer_postulate(request, num):
    offer        = get_object_or_404(Offer, id=num)
    offer_title  = offer.title
    offer_date   = offer.created
    offer_region = offer.get_region_display()
    
    owner        = offer.user
    owner_name   = offer.user.username
    owner_email  = offer.user.email
    
    sender       = request.user
    sender_name  = request.user.username
    sender_email = request.user.email


    static_files_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'static'))
    # get current website
    current_site = Site.objects.get_current()
    site_root    = current_site.domain
    full_offer_url = site_root +  offer.get_absolute_url()

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/logins/?next=%s'%offer.get_absolute_url() )

    # get the candidate profile linked to this user
    applyer = sender.profile_candid_set.latest('id')
    entreprise = owner.profile_emp_set.latest('id')

    # test if sender has written some motivations
    if applyer.motivations == None or len(applyer.motivations) < 1:
        msg = 'Veuillez exprimer un peu vos motivations pour le poste '
        return render_to_response('offre/offer.html', locals(), context_instance = RequestContext(request))

    motivations = applyer.motivations    

    if applyer in offer.profile_candid_set.all(): 
        msg = 'vous avez postulé pour l\'offre déja'
        return render_to_response('offre/offer.html', locals(), context_instance = RequestContext(request))    

    context = { 
                'nom':              sender_name, 
                'company':          owner_name,
                'titre':            offer_title, 
                'lieu':             offer_region, 
                'creattion_date':   offer_date 
               }

    images = ((os.path.join(static_files_path, 'images', 'logo1.png'), 'logo'), 
              (os.path.join(static_files_path, 'images', 'logo1.png'), 'logo')
              )

    subject = ugettext(u"SpeedJob: Votre candidature pour %s") % (offer_title)

    # send a confirmation email to the employer
    try:
        send_nice_email(
                    template_name ='html_email',
                    email_context = context,
                    subject       = subject,
                    recipients    = sender_email,
                    sender        = sender_name,
                    images        = images
                    )

    except:
        msg = 'L\'envoi de votre demande a echoué'
        return render_to_response('offre/offer.html', locals(), context_instance = RequestContext(request))    

    # send a copy to the employer
    context = { 
                 'nom':             sender_name, 
                 'company':         owner_name, 
                 'titre':           offer_title, 
                 'lieu':            offer_region, 
                 'creattion_date':  offer_date, 
                 'is_active':       offer.activated, 
                 'full_offer_url':  full_offer_url ,
                 'motivations'   :  motivations
                }

    subject = ugettext(u"SpeedJob: Le candidat : %s  vient de postuler pour votre offre: %s") % (sender_name, offer_title)

    try:
        send_nice_email(
                    template_name ='html_email_emp',
                    email_context = context,
                    subject       = subject,
                    recipients    = owner_email,
                    sender        = sender_name,
                    images        = images
                    )

    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        msg = 'L\'envoi de votre demande a echoué'
        return render_to_response('offer.html', locals(), context_instance = RequestContext(request))    

    msg = 'Votre demande a été envoyé avec succès'

    # create an application that joins the candidate and the offer 
    app = Application(offer=offer, person=applyer, company=entreprise )
    app.save()
    
    return render_to_response('offre/offer.html', locals(), context_instance = RequestContext(request))    

    
@login_required
def deposer_offre(request):
    # cars = Offer.objects.watermarked

    if request.method == 'POST':

        form = OfferForm(request.POST, request.FILES)

        if form.is_valid():
            title           = form.cleaned_data['title']
            offer           = form.cleaned_data['offer']
            category        = form.cleaned_data['category']
            region          = form.cleaned_data['region']
            salary          = form.cleaned_data['salary']
            
            immediate       = form.cleaned_data['immediate']    
            expired       = form.cleaned_data['expired']    
            description     = form.cleaned_data['description']  
            # image           = request.FILES['image']

            newcar = Offer( title           = title, 
                            offerType       = offer,
                            salary          = salary, 
                            category        = category, 
                            region          = region, 
                            immediate       = immediate, 
                            description     = description, 
                            expired         = expired, 
                            user            = request.user )
            newcar.save()

            messages.add_message(request, messages.INFO, ' Ajoutée avec succée .')
            return HttpResponseRedirect('/deposer_offre')
        else:
            messages.add_message(request, messages.ERROR, ' SVP complétez ou bien corrigez votre formulaire .')

    else:
        form = OfferForm()
    return render_to_response('offre/deposer_offre.html', locals(), context_instance = RequestContext(request))

def after_upload(request):
    return render_to_response('offre/after_upload.html', locals(), context_instance = RequestContext(request))

@login_required
def app_confirm(request, offer_id, user_id, app_id):
    
    app = Application.objects.get(id = app_id)
    app.is_seen = True
    app.save()
    # return redirect('emp_profile_offer_applyers', id=offer_id) 
    return HttpResponseRedirect('/applications')

@login_required
def app_reject(request, offer_id, user_id, app_id):
    
    app = Application.objects.get(id = app_id)
    app.is_seen = False
    app.save()
    # return redirect('emp_profile_offer_applyers', id=offer_id) 
    return HttpResponseRedirect('/applications')

@login_required
def applications(request):

    entreprise = Profile_emp.objects.get(user = request.user)

    apps = Application.objects.filter(company = entreprise)

    return render_to_response('profile/profile_emp_applications.html', locals(), context_instance=RequestContext(request))