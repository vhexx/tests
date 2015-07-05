from django.conf.urls import patterns, include, url
from django.contrib import admin
from tests import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/(?P<test_id>[0-9]*)/$', views.test),
    url(r'^question/(?P<question_id>[0-9]*)/$', views.prequestion),
    url(r'^$', views.index),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
