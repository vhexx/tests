from django.conf.urls import patterns, include, url
from django.contrib import admin
from tests import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/(?P<test_id>[0-9]*)/$', views.test),
    url(r'^question/(?P<question_id>[0-9]*)/$', views.question),
    url(r'^before_training/$', views.before_training),
    url(r'^training/(?P<training_image_pair_id>[0-9]*)/$', views.training),
    url(r'^after_training/$', views.after_training),
    url(r'^go_to_pairs/$', views.go_to_pairs),
    url(r'^pairs/$', views.pairs),
    url(r'^final/', views.final),
    url(r'^results/$', views.results),
    url(r'^$', views.index),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
