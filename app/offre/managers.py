import datetime
from django.db import models

class OfferQuerySets(models.query.QuerySet): 
        #here we define simple filters (or any queryset)
    def watermarked(self):
       return self.filter(is_watermarked = True)

    def is_activated(self):
       return self.filter(activated = True).order_by('-created')

    def index_is_activated(self):
       return self.filter(activated = True).order_by('-created')[:8]         

class OfferManager(models.Manager):
    def get_query_set(self):
        return OfferQuerySets(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

