from django.conf.urls import url
from . import views

app_name = 'Profile'

urlpatterns = [
    # Home
    url(r'^$', views.index, name='index'),

    # Profile
    url(r'^profile/$', views.profile, name='profile'),

    # Register
    url(r'^register/$', views.register, name='register'),

    # Login
    url(r'^login/$', views.log_in, name='login'),

    # Settings
    url(r'^settings/$', views.settings, name='settings'),

    # Logout
    url(r'^logout/$', views.log_out, name='logout'),
]
