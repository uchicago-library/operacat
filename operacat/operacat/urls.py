from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url, i18n
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
import os

from search import views as search_views
from dealerview import views as dealer_view

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

import registration

urlpatterns = [

    url(r'^django-admin/', admin.site.urls),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^accounts/', include('registration.backends.simple.urls'), name='register'),
    url(r'^accounts/password/reset/$', auth_views.PasswordResetView, {'template_name': 'templates/registration/password_reset.html'}, name="password_reset"),
    url(r'^accounts/password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    url('^login/', auth_views.LoginView, name='login'),
    url('^logout/', auth_views.LogoutView, name='logout'),

]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_ROOT)

urlpatterns += i18n_patterns(url(r'^search/$', search_views.search, name='search'),
                             url(r'^advanced_search/', search_views.advanced_search, name="advanced_search"),
                             url('^dealerbrowse/', dealer_view.browse, name='dealer-browse'),
                             url(r'^i18n/', include(i18n)),
                             url(r'', include(wagtail_urls))
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += [
        url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'operacat/images/favicon.ico'))
    ]
