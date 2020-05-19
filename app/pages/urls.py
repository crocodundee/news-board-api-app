from django.urls import path

from pages.views import HomePage

app_name = 'pages'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]
