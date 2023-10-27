from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static, serve
from django.views.generic.base import RedirectView
from .views import error_400, error_404, error_500, error_403

handler404 = error_404
#handler500 = error_500
handler403 = error_403
handler400 = error_400

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
sidmap_view = RedirectView.as_view(url='/static/sitemap.xml', permanent=True)

robot_view = RedirectView.as_view(url='/static/robots.txt', permanent=True)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('', include('chat.urls')),
    path('', include('post.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^favicon\.ico$', favicon_view),
    re_path(r'^sitemap\.xml$', sidmap_view),
    re_path(r'^robots\.txt$', robot_view),
]
