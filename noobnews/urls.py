"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from noobnews import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^cart/$', views.video_game_list_add, name='cart'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^videogamesuggest/(?P<videogame_name_slug>[\w\-]+)/$',
        views.suggestChanges, name='suggestChanges'),
    url(r'^suggest/$', views.suggest_category, name='suggest_category'),
    url(r'^videogame/(?P<videogame_name_slug>[\w\-]+)/$',
        views.show_videogame, name='show_videogame'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^reset_password/$', views.reset_password, name="reset_password"),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_password_confirm,name='reset_password_confirm'),
    url(r'^register/$', views.register, name='register'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url('', include('social_django.urls', namespace='social')),
    url(r'^top40/$', views.top40, name='top40'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
