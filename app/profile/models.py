# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from registration.signals import user_registered

from offre.models import Offer
from payments.models import Customer
from car_shop.random_unique import RandomPrimaryIdModel
from car_shop.model_choices import *
from django.db.models.signals import post_save
from django.dispatch import receiver

import subprocess
from django.conf import settings
from PyPDF2 import PdfFileReader, PdfFileWriter
from uuid import uuid4

profile_type = ((True, 'Candidat'), (False, 'Recruteur') )

class ExUserProfile(models.Model):
    user        = models.ForeignKey(User, unique=True)
    is_candid   = models.CharField(max_length=230)
 
    def __unicode__(self):
        return unicode(self.user)

class Profile_emp(RandomPrimaryIdModel):
    # id          = models.CharField(max_length=36, primary_key=True, default=lambda: ''.join([ i for i in str(uuid4()) if i != '-']) , editable=False)
    user        = models.ForeignKey(User, unique=True)
    is_candid   = models.CharField(max_length=230)

    class Meta:
        verbose_name        = "Employeur"
        verbose_name_plural = 'Emplyeurs'

    def __unicode__(self):
        return unicode(self.user)

    representant = models.CharField(max_length=230, null=True, blank=True)  
    siret        = models.CharField(max_length=230, null=True, blank=True)  
    created_at   = models.DateTimeField(verbose_name="Date de creation",        auto_now_add = True)
    society      = models.CharField(verbose_name="Société",     max_length=200, null=True, blank=True)
    phone        = models.CharField(verbose_name="Téléphone",   max_length=200, null=True, blank=True)
    postal_code  = models.CharField(verbose_name="Code postal", max_length=200, null=True, blank=True)
    town         = models.CharField(verbose_name="Ville",       max_length=200, null=True, blank=True)
    website      = models.CharField(verbose_name="Site Web",    max_length=200, null=True, blank=True)
    presentation = models.TextField(verbose_name="Présentation",                null=True, blank=True)

    def __unicode__(self):
        return unicode(self.user)

    def get_payement_status(self):
        employer = self.user
        try:
            customer = Customer.objects.get(user=employer)
            subscription = customer.current_subscription
            status   = subscription.status

        except Customer.DoesNotExist:    
            return None

        return status

    def can_download(self):
        employer = self.user
        try:
            customer = Customer.objects.get(user=employer)
            subscription = customer.current_subscription
            status   = subscription.status

            if status == "active":
                return True
            elif subscription.status == "canceled" and subscription.is_period_current():
                return True    

        except Customer.DoesNotExist:    
            return False

        return False    

    def get_offers(self):
        offers = self.user.offer_set.all()
        return offers

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:

            fname = f.name        
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_'+fname+'_display'
            if hasattr( self, get_choice): value = getattr( self, get_choice)()
            else:
                try : value = getattr(self, fname)
                except User.DoesNotExist: value = None

            # only display fields with values and skip some fields entirely
            if f.editable and value and f.name not in ('id', 'user', 'is_candid', 'created_at', 'presentation') :
                fields.append( f.name )

        keys = ['society', 'phone', 'postal_code', 'town', 'website']

        msg = None
        print fields
        for i in keys:
            if not i in fields:
                msg = 'Veuillez completer votre profile s\'il vous plait ' 
                break
            else:
                continue 
        return msg

    def is_there_non_confirmed_app(self):
        result = False
        for i in self.application_set.all():
            print i
            if not i.is_seen:
                result = True
                break

        return result    


class Profile_candid(RandomPrimaryIdModel):
    # id          = models.CharField(max_length=36, primary_key=True, default=lambda: ''.join([ i for i in str(uuid4()) if i != '-']) , editable=False)
    user          = models.ForeignKey(User, unique=True)
    offer         = models.ManyToManyField(Offer, verbose_name="a postulé pour ",  null=True, blank=True, through = "Application" )

    is_candid     = models.CharField(max_length=230)

    prenom        = models.CharField(max_length=230, null=True, blank=True,default="")  
    last_name     = models.CharField(verbose_name = u'Nom de famille', max_length=200, null=True, blank=True, default="")
    created_at    = models.DateTimeField(verbose_name=u'Ajouté le', auto_now_add=True)
    adress        = models.CharField(verbose_name = u'Adresse', max_length=200, null=True, blank=True, default="")
    telephone     = models.CharField(verbose_name = u'Telephone', max_length=200, null=True, blank=True)
    # recently added fields
    sector1       = models.CharField(verbose_name = u'Secteur 1', max_length = 200,choices=CATEGORY_CHOICES, null=True, blank=True, default='0')
    sector2       = models.CharField(verbose_name = u'Secteur 2', max_length = 200,choices=CATEGORY_CHOICES, null=True, blank=True,default='0')
    sector3       = models.CharField(verbose_name = u'Secteur 3', max_length = 200,choices=CATEGORY_CHOICES, null=True, blank=True, default='0')
    # mobility
    mobility1     = models.CharField(verbose_name = u'Mobilité 1', max_length = 200,choices=DEPARTEMENT_CHOICES, null=True, blank=True, default='0')
    mobility2     = models.CharField(verbose_name = u'Mobilité 2', max_length = 200,choices=DEPARTEMENT_CHOICES, null=True, blank=True, default='0')
    mobility3     = models.CharField(verbose_name = u'Mobilité 3', max_length = 200,choices=DEPARTEMENT_CHOICES, null=True, blank=True, default='0')
    
    disponibility = models.CharField(verbose_name = u'Disponibilité', max_length = 200,choices=DISPONIBILITY_CHOICES, null=True, blank=True, default='0')
    
    status        = models.CharField(verbose_name = u'Status', max_length = 200, choices=STATUS_CHOICES, null=True, blank=True ,default='0') 
    salary        = models.CharField(verbose_name = u'Salaire', max_length = 200, choices=SALARY_CHOICES, null=True, blank=True ,default='0') 
    
    study_level   = models.CharField(verbose_name = u'Niveau d\'etudes', max_length = 200, choices=STUDY_LEVEL_CHOICES, null=True, blank=True ,default='0') 
    experience    = models.CharField(verbose_name = u'Experience', max_length = 200, choices=EXPERIENCE_CHOICES,  null=True, blank=True ,default='0') 
    contract      = models.CharField(verbose_name = u'Contrat', max_length = 200, choices=OFFER_CHOICES, null=True,  blank=True,default='0') 
    period        = models.CharField(verbose_name = u'periode', max_length = 200, choices=PERIOD_CHOICES, null=True, blank=True,default='0') 
    
    languages     = models.CharField(verbose_name = u'langues', max_length=200, null=True, blank=True, default='')
    document      = models.FileField(verbose_name = u'CV', upload_to = 'uploads/pdfs/', null=True, blank=True)
    motivations   = models.TextField(verbose_name = u'motivations',                null=True, blank=True)

    class Meta:
        verbose_name        = "Candidat"
        verbose_name_plural = 'Candidats'
 
    def __unicode__(self):
        return unicode(self.user)

    def get_pdf_image(self):
        the_file = self.document.file.name.split('/')[-1].split('.')[0]
        return '%s/pdfs_images/img-%s.jpg' %( "/".join(self.document.file.name.split('/')[:-2] ), the_file)

    def get_absolute_url(self):
        return '/candidate/%s'%(self.id)

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:

            fname = f.name        
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_'+fname+'_display'
            if hasattr( self, get_choice): value = getattr( self, get_choice)()
            else:
                try : value = getattr(self, fname)
                except User.DoesNotExist: value = None

            # only display fields with values and skip some fields entirely
            if f.editable and value and f.name not in ('id', 'workshop', 'user', 'complete', 'is_candid') :
                fields.append( f.name )

        keys = ['last_name', 'adress', 'telephone', 'sector1', 'sector2', 'sector3', 'mobility1', 'mobility2', 'mobility3', 'disponibility', 'status', 'salary', 'study_level', 'experience', 'contract', 'period', 'languages']    

        msg = None
        for i in keys:
            if not i in fields:
                msg = 'Veuillez completer votre profile s\'il vous plait ' 
                break
            else:
                continue 
        return msg

    def is_my_application_confirmed(self, offer_id):
        # apli = 
        return False    


    
def pdf_post_save(sender, instance=False, **kwargs):

    pdf = Profile_candid.objects.get(pk=instance.pk)
    if pdf.document:
        new_name =  pdf.document.file.name.split('/')[-1].split('.')[0]

        output = PdfFileWriter()
        pdfOne = PdfFileReader(file( '%s/%s' % (settings.MEDIA_ROOT, pdf.document), "rb"))
        output.addPage(pdfOne.getPage(0))

        outputStream = file(r'%s/uploads/first/%s-first.pdf'  % (settings.MEDIA_ROOT, new_name), "wb")
        output.write(outputStream)
        outputStream.close()

        params = ['convert', 
                    '-blur' ,'4x6',
                    (r'%s/uploads/first/%s-first.pdf')  % (settings.MEDIA_ROOT, new_name),
                     '%s/uploads/pdfs_images/img-%s.jpg' % (settings.MEDIA_ROOT, new_name )
                     ]
        subprocess.check_call(params)

post_save.connect(pdf_post_save, sender=Profile_candid)       


# this called after creation of temporary user
def user_registered_callback(sender, user, request, **kwargs):
    profile = ExUserProfile(user = user)
    profile.is_candid = request.POST["is_candid"]

    if profile.is_candid == '1':  ##### try to use it later to make an easy check of users type
        c = Profile_candid(user = user, is_candid ='yes')
        #add user to candidate group
        gr = Group.objects.get(name='candidate')
        gr.user_set.add(user)
        c.save()
    elif profile.is_candid == '0': 
        c = Profile_emp(user = user, is_candid ='no', society = user.username)
        # add user to employer group
        gr = Group.objects.get(name='employer')
        gr.user_set.add(user)    
        c.save()

user_registered.connect(user_registered_callback)


class Application(models.Model):
    offer   = models.ForeignKey(Offer, verbose_name="offre")
    person  = models.ForeignKey(Profile_candid, verbose_name="Candidat")
    company = models.ForeignKey(Profile_emp, verbose_name="entreprise")
    created = models.DateTimeField(verbose_name= "date de candidature", auto_now_add=True)
    is_seen = models.BooleanField(verbose_name='Vue', default=False)

    class Meta:
        verbose_name = 'candidature'

    def __unicode__(self):
        return unicode(('User: %s offer: %s') %(self.person.user.username, self.offer.title))   

