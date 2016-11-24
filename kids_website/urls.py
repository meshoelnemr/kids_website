from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Home / profile
    url(r'^', include('Profile.urls')),

    # Games
    url(r'^games/', include('games.urls')),
]
