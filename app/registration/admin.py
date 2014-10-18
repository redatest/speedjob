# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from profile.models import ExUserProfile, Profile_emp, Profile_candid, Application

from registration.models import RegistrationProfile

class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        
        """
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.
        
        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = _("Re-send activation emails")

class CandidInline(admin.TabularInline):
    model = Profile_candid.offer.through #Herein lies the trick. To get the manytomany relationship to show up in the admin, use "through"
    extra = 0 # do not display extra proposistions

class Profile_candid_admin(admin.ModelAdmin):

    readonly_fields = ("created_at",) 
    fieldsets = (

    ( 'Infos générales:',       {'fields': [ 'prenom', 'last_name', 'adress', 'telephone', "created_at" ] }),
    ( 'Secteur de recherche:',  {'fields': [ ('sector1', 'sector2', 'sector3')],        'classes': ['extrapretty'] }),
    ( 'Mobilité:',              {'fields': [ ('mobility1', 'mobility2', 'mobility3') ], 'classes': ['extrapretty'] }),
    ( 'Autres Infos:',          {'fields': ['disponibility', 'status', 'salary' , 'study_level', 'experience' , 'contract', 'period' , 'languages' ],'classes': ['extrapretty'] }),
    ( 'Motivations:',          {'fields': [ ('motivations') ],'classes': ['extrapretty'] }),

     )
    # raw_id_fields = ('applies',) # to disable querying all offers , we print only the linked one (goes well with ForeignKey field)
    # filter_horizontal = ('applies',) # this will create 2 table to filter objects horazontally
    # filter_vertical = ('applies',) # this will create 2 table to filter objects vertically

    list_filter   = ('last_name',)
    list_display  = ('last_name', 'prenom', 'created_at', 'experience', 'status')
    exclude       = ('is_candid', 'offer', )  # exclude applies to avoid showing it twice
    inlines       = [ CandidInline,]
    date_hierachy = ('-created_at',)
    ordering      = ('-created_at',)

class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields  = ['offer', 'person', 'company', "created", 'is_seen']
    list_display     = ['__unicode__', 'company', 'created', 'is_seen']

admin.site.register(RegistrationProfile, RegistrationAdmin)
admin.site.register(Profile_emp)
admin.site.register(Profile_candid, Profile_candid_admin)
admin.site.register(Application, ApplicationAdmin)