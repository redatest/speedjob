# -*- coding: utf-8 -*-                 
from django.db import models
# from car_shop.fields import ThumbnailImageField 
from car_shop.model_choices import *
from car_shop.random_unique import RandomPrimaryIdModel
import datetime
import math
from offre.managers import OfferManager
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from uuid import uuid4
import subprocess
from django.conf import settings
from PyPDF2 import PdfFileReader, PdfFileWriter

from datetime import date, timedelta

from django.db.models.signals import post_save, post_delete
from caching.caching import cache_update, cache_evict


class Offer(RandomPrimaryIdModel):
    """ Modele pour les offres de travail """
    # id          = models.CharField(max_length=36, primary_key=True, default=lambda: ''.join([ i for i in str(uuid4()) if i != '-']) , editable=False)
    user        = models.ForeignKey(User)
    
    title       = models.CharField(max_length=250)
    offerType   = models.CharField( _('type de l\'offre '), max_length = 200, choices=OFFER_CHOICES, default='1')
    category    = models.CharField( _('categorie'), max_length = 200, choices=CATEGORY_CHOICES, default='1')
    region      = models.CharField(max_length = 200, choices=REGION_CHOICES)
    salary      = models.CharField( _('salaire'), max_length = 200, blank=True, choices=SALARY_CHOICES)
    
    views       = models.CharField(_('Nombre de vues'),max_length = 200, blank=True, default=0)
    description = models.TextField(_('description'), blank=True, null=True)
    
    created     = models.DateTimeField(_('date de creation'), null=True)
    modified    = models.DateTimeField(_('date de modification'), null=True)
    expired     = models.DateTimeField(_('date d\'expiartion '), null=True)
    immediate   = models.CharField(max_length = 20, choices=YESNO, default='1')
    
    activated   = models.BooleanField(_('Activee'), blank=True, default=True)

    class Meta:
        verbose_name        = _('Offre')
        verbose_name_plural = _('Offres')
    
    def __unicode__(self):
        return unicode(self.title)

    def is_available(self):
        day_count = (self.expired - self.created).days + 1
        return day_count >= 0

    def remaining_days(self):
        day_count = (self.expired - self.created).days + 1
        return day_count

    def get_applyers_count(self):
        return self.profile_candid_set.count()    

    def head_summary(self):
        LIMIT = 80
        tail = len(self.description) > LIMIT and '......' or ''
        return self.description[:LIMIT] + tail    

    def tooltip_head_summary(self):
        LIMIT = 280
        tail = len(self.description) > LIMIT and '......' or ''
        return self.description[:LIMIT] + tail        

    def get_absolute_url(self): return '/offer/%s' %(self.id)

    def get_disable_url(self): return '/offer/%s/disable' %(self.id)

    def get_activation_url(self): return '/offer/%s/activate' %(self.id)

    def get_edition_url(self): return '/offer/%s/edit' %(self.id)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id: self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(Offer, self).save(*args, **kwargs) 
    
    # this a function for the image list display
    def image_tag(self):

        return u'<img src="%s" width="80" height="80" />' % self.image.url
        image_tag.short_description = 'Image'

    image_tag.allow_tags = True 

    objects = OfferManager() # pour avoir que les objets active: Offer.objects.is_watermaked
    # objects = models.Manager() # On garde le manager par default

    @property
    def cache_key(self):
        return self.get_absolute_url()

post_save.connect(cache_update, sender=Offer)
post_delete.connect(cache_evict, sender=Offer)


