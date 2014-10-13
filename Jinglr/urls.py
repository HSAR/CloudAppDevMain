from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import TemplateView
import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^$', TemplateView.as_view(template_name='home.html')),
    ('^admin/', include(admin.site.urls)),
)
