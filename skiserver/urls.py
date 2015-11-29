from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'skibuddy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^checkUser/', 'skibuddy.views.check_user', name='check_user'),
    url(r'^createEvent/', 'skibuddy.views.create_event', name='create_event'),
    url(r'^fetchEvent/', 'skibuddy.views.event_details', name='event_details'),
    url(r'^joinEvent/', 'skibuddy.views.join_event', name='join_event'),
    url(r'^admin/', include(admin.site.urls)),
)
