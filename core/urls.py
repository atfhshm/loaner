"""core URL Configuration"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.extend(
        urlpattern
        for urlpattern in (
            # the * start before static is used for sequence unpacking
            # because static returns a list of urlpatterns
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
            path("api-auth/", include("rest_framework.urls")),
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            path(
                "api/schema/docs/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="schema-docs",
            ),
        )
    )
