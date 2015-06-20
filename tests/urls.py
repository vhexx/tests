from django.conf.urls import patterns, include, url
from django.contrib import admin
from tests import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test$', views.test),
    url(r'^question$', views.question),
    url(r'^$', views.index),
)
