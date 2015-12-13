from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'skibuddy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^checkUser/', 'skibuddy.views.check_user', name='check_user'),
    url(r'^getUsersInfo/', 'skibuddy.views.get_userInfo', name='get_userInfo'),
    url(r'^startSession/', 'skibuddy.views.start_session', name='add_session'),
    url(r'^createEvent/', 'skibuddy.views.create_event', name='create_event'),
    url(r'^fetchEvent/', 'skibuddy.views.event_details', name='event_details'),
    url(r'^joinEvent/', 'skibuddy.views.join_event', name='join_event'),
    url(r'^getEvent/', 'skibuddy.views.get_events', name='get_event'),
    url(r'^unjoinEvent/', 'skibuddy.views.unjoin_event', name='unjoin_event'),
    url(r'^updateLocation/', 'skibuddy.views.update_currentloc', name='update_currentloc'),
    url(r'^getSkirecords/', 'skibuddy.views.get_skirecords', name='get_skirecords'),
    url(r'^endSession/', 'skibuddy.views.end_session', name='end_session'),
    url(r'^getEventMembers/', 'skibuddy.views.get_eventmembers', name='end_session'),
    url(r'^admin/', include(admin.site.urls)),
)
