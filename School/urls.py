from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
#  import django.contrib.auth.views

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    # url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^rank/', include('rank.urls')),
    url(r'', include('blog.urls')),
]

# if settings.DEBUG:
#     urlpatterns += url(r'^media/(?P<path>.*)', 'django.views.static', {'document_root': settings.MEDIA_ROOT})
