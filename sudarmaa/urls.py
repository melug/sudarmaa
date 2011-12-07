from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"", include('books.urls')),
    url(r"", include('dictionary.urls')),
    url(r"", include('gallery.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^photologue/', include('photologue.urls')),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    # social auth
    url(r"^", include('social_auth.urls')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
    urlpatterns += patterns('',
        url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
