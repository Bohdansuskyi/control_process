
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # include app urls
    path("",include("app.urls")),
    path('admin/', admin.site.urls),
]