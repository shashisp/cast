from django.conf.urls import patterns, include, url
from main.views import IndexView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view()),
    # url(r'^cast/', include('cast.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^submit/', 'main.views.submit'),
    url(r'^admin/', include(admin.site.urls)),
)
