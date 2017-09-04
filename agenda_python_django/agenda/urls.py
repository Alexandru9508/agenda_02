from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # url for login
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name='login'),
    # url for logout
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'},
        name='logout'),
    # url for signup
    url(r'^signup/$', views.signup, name='signup'),
    # url for email activation
    url(r'^account_activation_sent/$', views.account_activation_sent,
        name='account_activation_sent'),
    # url for activate email
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    # url change password
    url(r'^password_reset/$', auth_views.password_reset,
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),

    # creare inregistrare
    url(r'^create_event/$', views.create_event, name='create_event'),

    # url /username
    # url(r'^(?P<user>[a-z]+)/$', views.IndexView.as_view(),
    #     name='username'),
    # # # detail
    # url(r'^(?P<user>[a-z]+)/(?P<pk>[0-9]+)/$', views.DetailView.as_view(),
    #     name='detail'),

]
