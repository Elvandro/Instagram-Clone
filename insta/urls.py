from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^post/', views.post, name='post'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'^search/', views.search_result, name='search'),
    url(r'^like/(?P<operation>.+)/(?P<pk>\d+)', views.like, name='like'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^updateprofile/', views.update_profile, name='edit'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
