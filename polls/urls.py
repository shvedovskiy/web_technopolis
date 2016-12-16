from django.conf.urls import url
from django.contrib.auth import login, logout
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),  # /polls/
    url(r'^new/$', views.CreateView.as_view(), name='new'),  # /polls/new/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),  # /polls/5/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),  # /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),  # /polls/5/vote/
    url(r'^login/', login, {'template_name': 'core/login.html'}),
]
