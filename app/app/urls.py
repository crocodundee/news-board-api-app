from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

API_TITLE = 'News board API'
API_DESC = 'A Web API to create news posts'
schema_view = get_schema_view(title=API_TITLE)


urlpatterns = [
    path('', include('pages.urls')),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESC)),
    path('schema/', schema_view, name='api-schema'),
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls")),
    path("api/news/", include("news.urls")),
]
