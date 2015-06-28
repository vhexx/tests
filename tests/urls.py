from django.conf.urls import patterns, include, url
from django.contrib import admin
from tests import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/(?P<test_id>[0-9]*)/$', views.test),
    url(r'^prequestion/(?P<question_id>[0-9]*)/$', views.prequestion),
    url(r'^$', views.index),
)
