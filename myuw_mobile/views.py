from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
import logging
from myuw_api.sws_dao import Quarter
from myuw_api.pws_dao import Person as PersonDAO

logger = logging.getLogger('myuw_mobile.views')


#@mobile_template('{mobile/}index.html')
def index(request):
    context = {'year': None,
               'quarter': None,
               'regid': None,
               'myuw_base_url': '',
               'err': None}

    if settings.DEBUG:
        netid = 'javerage'
    else:
        netid = request.user.username

        if netid is None:
            raise("Must have a logged in user when DEBUG is off")

    person_dao = PersonDAO()
    try:
        person = person_dao.get_person_by_netid(netid)
        request.session["user_netid"] = person.uwnetid
    except Exception, message:
        logger.error(message)
        context['err'] = 'Failed to get regid'

    try:
        cur_term = Quarter().get_cur_quarter()
    except Exception, message:
        logger.error(message)
        context['err'] = 'Failed to get quarter '
    else:
        context['year'] = cur_term.year
        context['quarter'] = cur_term.quarter

    return render_to_response('index.html',
                              context,
                              context_instance=RequestContext(request))

def myuw_login(request):

    if settings.DEBUG:
        netid = 'javerage'
    else:
        netid = request.user.username

        if netid is None:
            raise("Must have a logged in user when DEBUG is off")

    person_dao = PersonDAO()
    try:
        person = person_dao.get_person_by_netid(netid)

    except Exception, message:
        logger.error(message)
        context['err'] = 'Failed to get regid'

    if person.is_student:
        return redirect("myuw_mobile.views.index")

    if hasattr(settings, "MYUW_USER_SERVLET_URL"):
        return redirect(settings.MYUW_USER_SERVLET_URL)
    else:
        return redirect("https://myuw.washington.edu/servlet/user"
                           "?defbut=Log+in+with+your+UW+NetID")


