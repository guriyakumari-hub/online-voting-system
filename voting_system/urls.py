from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

def home(request):
    return HttpResponse("Welcome to Online Voting System 🚀")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
