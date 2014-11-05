from django.conf import settings
from profile.models import Profile_emp
from django.utils.translation import ugettext_lazy as _

def is_there_emplyer_notif(request):
    """ context processor for the site templates """

    # test if there is notification for employers
    if request.user.is_authenticated():
        u = request.user
        if u.groups.filter(name="employer"):
            profile = Profile_emp.objects.get(user = u)
            result  = u.profile_emp_set.all()[0].is_there_non_confirmed_app()

    return {'request': request, 'is_there_emplyer_notif': result }

