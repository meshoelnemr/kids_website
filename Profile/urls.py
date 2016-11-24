from django.conf.urls import url
from . import views

app_name = 'Profile'

urlpatterns = [
    # Home / profile
    url(r'^$', views.index, name='index'),
    # Register
    url(r'^register/$', views.register, name='register'),
    # Login
    url(r'^login/$', views.log_in, name='login'),
    # Logout
    url(r'^logout/$', views.log_out, name='logout'),
]
