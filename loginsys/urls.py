from django.conf.urls import url
from . import views

app_name = 'loginsys'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
]
