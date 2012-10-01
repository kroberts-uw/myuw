from django.conf.urls import patterns, include, url
from myuw_mobile.views.page import index
from myuw_mobile.views.mobile_login import user_login
from myuw_mobile.views.support import support
from myuw_mobile.views.schedule_api import StudClasScheCurQuar
from myuw_mobile.views.contact_api import InstructorContact
from myuw_mobile.views.textbook_api import TextbookCurQuar
from myuw_mobile.views.links_api import QuickLinks

urlpatterns = patterns('myuw_mobile.views',
    url(r'login', 'mobile_login.user_login'),
    url(r'support', 'support.support'),
    url(r'^visual', 'page.index'),
    url(r'^textbooks', 'page.index'),
    url(r'^instructor', 'page.index'),
    url(r'^links', 'page.index'),
    url(r'^$', 'page.index'),
    url(r'^api/v1/books/current/$', TextbookCurQuar().run),
    url(r'^api/v1/schedule/current/$', StudClasScheCurQuar().run),
    url(r'^api/v1/links/$', QuickLinks().run),
    url(r'^api/v1/person/(?P<regid>.*)$', InstructorContact().run),
)
