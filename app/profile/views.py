# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect

# models and forms
from offre.models import Offer
from article.models import Article
from car_shop.forms import Search_Form, Text_Search_Form
from profile.models import Profile_candid, Profile_emp
from profile.forms import UserInfoForm, EmployerInfoForm

# pagination ans search
from django.db.models import F
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
# from decorators.auth import group_required

#utils
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from django.core.context_processors import csrf
from django.utils import translation

@login_required
def candid_profile(request):
    
    usname 		= request.user.username
    uslname 	= request.user.last_name
    userinfo 	= Profile_candid.objects.get( user = request.user )

    if request.method == 'POST':

        # form 	= UserInfoForm(data=request.POST, instance=userinfo, user=request.user)
        form 	= UserInfoForm(data=request.POST,  user=request.user)
        if form.is_valid():
            form.save()
            message = messages.add_message(request, messages.INFO, 'données enregistrées avec succée')
            return HttpResponseRedirect('/profile/')
        else:
            message = messages.add_message(request, messages.INFO, 'erreur durant la savegarde  ')
            return render_to_response('profile.html', locals(), context_instance=RequestContext(request))

    else: 
        # use form initial
        # form = UserInfoForm(instance=userinfo, user=request.user)
        form = UserInfoForm(user=request.user)
        userinfo = Profile_candid.objects.get( user = request.user )
        return render_to_response('./profile/profile.html', locals(), context_instance=RequestContext(request))

@login_required
def candid_profile_edit(request, id):

    userinfo = Profile_candid.objects.get(id = id)

    if request.method=='POST':
        form = UserInfoForm(request.POST, request.FILES)

        if form.is_valid():

            userinfo.prenom        = form.cleaned_data['prenom']
            userinfo.adress        = form.cleaned_data['adress']
            userinfo.last_name     = form.cleaned_data['last_name']
            userinfo.telephone     = form.cleaned_data['telephone']
            userinfo.sector1       = form.cleaned_data['sector1']
            userinfo.sector2       = form.cleaned_data['sector2']
            userinfo.sector3       = form.cleaned_data['sector3']
            userinfo.mobility1     = form.cleaned_data['mobility1']
            userinfo.mobility2     = form.cleaned_data['mobility2']
            userinfo.mobility3     = form.cleaned_data['mobility3']
            userinfo.disponibility = form.cleaned_data['disponibility']
            userinfo.status        = form.cleaned_data['status']
            userinfo.salary        = form.cleaned_data['salary']
            userinfo.study_level   = form.cleaned_data['study_level']
            userinfo.experience    = form.cleaned_data['experience']
            userinfo.contract      = form.cleaned_data['contract']
            userinfo.period        = form.cleaned_data['period']
            userinfo.languages     = form.cleaned_data['languages']
            userinfo.motivations   = form.cleaned_data['motivations']

            userinfo.save()
        else:
            print form.errors

        return HttpResponseRedirect('/candid_profile')
    else:
        form = UserInfoForm(initial = {
                            'prenom'        : userinfo.prenom,
                            'adress'        : userinfo.adress,
                            'last_name'     : userinfo.last_name,
                            'telephone'     : userinfo.telephone,
                            'sector1'       : userinfo.sector1,
                            'sector2'       : userinfo.sector2,
                            'sector3'       : userinfo.sector3,
                            'mobility1'     : userinfo.mobility1,
                            'mobility2'     : userinfo.mobility2,
                            'mobility3'     : userinfo.mobility3,
                            'disponibility' : userinfo.disponibility,
                            'status'        : userinfo.status,
                            'salary'        : userinfo.salary,
                            'study_level'   : userinfo.study_level,
                            'experience'    : userinfo.experience,
                            'contract'      : userinfo.contract,
                            'period'        : userinfo.period,
                            'languages'     : userinfo.languages,
                            'document'      : userinfo.document,
                            'motivations'   : userinfo.motivations
            })
    return render_to_response('./profile/profile_edit.html', locals(), context_instance = RequestContext(request))


@login_required
def emp_profile_edit(request, id):

    userinfo = Profile_emp.objects.get(id = id)

    if request.method=='POST':
        form = EmployerInfoForm(request.POST, request.FILES)

        if form.is_valid():

            userinfo.representant = form.cleaned_data['representant']
            userinfo.siret        = form.cleaned_data['siret']
            userinfo.phone        = form.cleaned_data['phone']
            userinfo.postal_code  = form.cleaned_data['postal_code']
            userinfo.town         = form.cleaned_data['town']
            userinfo.website      = form.cleaned_data['website']
            userinfo.presentation = form.cleaned_data['presentation']

            userinfo.save()
        else:
            print form.errors

        return HttpResponseRedirect('/emp_profile')
    else:
        form = EmployerInfoForm(initial = {
                            'representant'      : userinfo.representant,
                            'siret'             : userinfo.siret,
                            'phone'             : userinfo.phone,
                            
                            'postal_code'       : userinfo.postal_code,
                            'town'              : userinfo.town,
                            'website'           : userinfo.website,
                            'presentation'      : userinfo.presentation
                            
            })
    return render_to_response('./profile/profile_emp_edit.html', locals(), context_instance = RequestContext(request))



@login_required
# @user_passes_test(lambda u: u.groups.filter(name='employer').count() == 0, login_url='/')
def emp_profile(request):
    usname 		= request.user.username
    uslname 	= request.user.last_name
    userinfo 	= Profile_emp.objects.get( user = request.user )

    if request.method == 'POST':
        # form = Profile_emp(data=request.POST, instance=userinfo, user=request.user)
        form = Profile_emp(data=request.POST,  user=request.user)
        if form.is_valid():
            form.save()
            message = messages.add_message(request, messages.INFO, 'données enregistrées avec succée')
            return HttpResponseRedirect('/profile/')
        else:
            message = messages.add_message(request, messages.INFO, 'erreur durant la savegarde  ')
            return render_to_response('./profile/profile.html', locals(), context_instance=RequestContext(request))
    else: 
        # use form initial
        # form = Profile_emp(instance=userinfo, user=request.user)
        form = EmployerInfoForm(user=request.user)
        userinfo = Profile_emp.objects.get( user = request.user )
        return render_to_response('./profile/profile_emp.html', locals(), context_instance=RequestContext(request))

@login_required
def emp_profile_offres(request):
    
    usname      = request.user.username
    uslname     = request.user.last_name
    userinfo    = Profile_emp.objects.get( user = request.user )
    offers      = userinfo.get_offers().order_by('-created')

    return render_to_response('./profile/profile_emp_offers.html', locals(), context_instance=RequestContext(request))

@login_required
def emp_profile_offer_applyers(request, id):
    
    offer       = Offer.objects.get(id=id)
    applyers    = offer.profile_candid_set.all()

    usname      = request.user.username
    uslname     = request.user.last_name
    userinfo    = Profile_emp.objects.get( user = request.user )

    return render_to_response('./profile/profile_emp_offer_applyers.html', locals(), context_instance=RequestContext(request))


@login_required
def candidate(request, num):
    userinfo = Profile_candid.objects.get(id=num)
    return render_to_response('./profile/candidate.html', locals(), context_instance=RequestContext(request))


def search_candidates(request):
    # preparing forms
    text_form   = Text_Search_Form()
    form        = Search_Form()
    
    users = Profile_candid.objects.all()

    articles  = users
    paginator = Paginator(articles, 15) 
    page      = request.GET.get('page')
    #paginating found users
    try: contacts = paginator.page(page)
    except PageNotAnInteger:    contacts = paginator.page(1)
    except EmptyPage:           contacts = paginator.page(paginator.num_pages)
    return render_to_response('./profile/search_candidates.html', locals(), context_instance = RequestContext(request) )


