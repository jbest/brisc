from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rapid_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^inventory/', include('rapid.urls')),
    url(r'^', include('rapid.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout),
    #url(r'^chaining/', include('smart_selects.urls')),
)

