# -*- coding: utf-8 -*-
from django.conf.urls import *
from profile.forms import ExRegistrationForm
from registration.backends.default.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from django.contrib import admin

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',

    # main application
    url('^$', "car_shop.views.home", name='home'),
    
    # payment application
    (r'pay/', include('main.urls')),

    (r'^admin/', include(admin.site.urls)),

    url(r"^payments/", include("payments.urls")),


    # offres
    url('^deposer_offre$', "offre.views.deposer_offre", name='deposer_offre'),

    url('^after_upload$', "offre.views.after_upload", name='after_upload'),

    url('^offer/(?P<num>\w+)/$', "offre.views.offer", name='offer'),

    url('^offer/(?P<num>\w+)/edit/$', "offre.views.offer_edit", name='offer_edit'),

    url('^offer/(?P<num>\w+)/disable/$', "offre.views.offer_disable", name='offer_disable'),    

    url('^offer/(?P<num>\w+)/activate/$', "offre.views.offer_activate", name='offer_activate'),

    url('^offer/(?P<num>\w+)/postulate/$', "offre.views.offer_postulate", name='offer_postulate'),    

    # application
    url('^applications/$', "offre.views.applications", name='applications'),

    url('^application/(?P<offer_id>\w+)/confirm/(?P<user_id>\w+)/set/(?P<app_id>\w+)$', "offre.views.app_confirm", name='app_confirm'),

    url('^application/(?P<offer_id>\w+)/reject/(?P<user_id>\w+)/set/(?P<app_id>\w+)/$', "offre.views.app_reject", name='app_reject'),    

    # article
    url('^news$', "article.views.news", name='news'),

    url('^news_item/(?P<num>\w+)/$', "article.views.news_item", name='news_item'),

    url('^contact$', "car_shop.views.contact", name='contact'),

    # searching
    url('^search$', "car_shop.views.search", name='search'),

    url(r'^search/$', "car_shop.views.search", name='search'),
    
    url(r'^map_search/$', "car_shop.views.map_search", name='map_search'),

    url(r'^search_candidates/$', "profile.views.search_candidates", name='search_candidates'),
    
    # Profile
    url(r'^candid_profile/$', "profile.views.candid_profile", name='candid_profile'),    

    url(r'^candid_profile_edit/(?P<id>\w+)/$', "profile.views.candid_profile_edit", name='candid_profile_edit'),    

    url(r'^emp_profile/$', "profile.views.emp_profile", name='emp_profile'),    

    url(r'^emp_profile_offres/$', "profile.views.emp_profile_offres", name='emp_profile_offres'),    

    url(r'^emp_profile_edit/(?P<id>\w+)/$', "profile.views.emp_profile_edit", name='emp_profile_edit'),    

    url(r'^emp_profile_offer_applyers/(?P<id>\w+)/$', "profile.views.emp_profile_offer_applyers", name='emp_profile_offer_applyers'),    
    
    url(r'^candidate/(?P<num>\w+)/$', "profile.views.candidate", name='candidate'),    

    # daxice 
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # custom registration
    url(r'accounts/register/$', RegistrationView.as_view(form_class = ExRegistrationForm), name = 'registration_register'),

    url(r'accounts/login/$', 'registration.views.login', name = 'authentication_login'),

    (r'^accounts/', include('registration.backends.default.urls')),

)

urlpatterns += patterns('',
        url(r'media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT, }),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

