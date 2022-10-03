"""sleek_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # the include allows us to connect the urls form the home app to the project urls
from django.conf import settings # importing the the static changes from settings
from django.conf.urls.static import static # importing static itself from the settings so as to modify it in this url.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), # this is allows us to make changes in the home app urls.py and also reflect here
]

# A condition fro our static and media files so that they can show when we insert the url in the webpage
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)