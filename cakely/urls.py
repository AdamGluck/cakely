from django.conf.urls import patterns, include, url

from django.contrib import admin

from apps.views import HomePageView, SeeLikeHistoryView, RunView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^historical/', SeeLikeHistoryView.as_view(), name='historical'),
    url(r'^run/', RunView.as_view(), name='run'),
    url(r'^admin/', include(admin.site.urls)),
)
