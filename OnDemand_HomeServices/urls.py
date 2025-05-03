from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

from django.urls import path
from django.http import HttpResponse
from django.core.management import call_command

def trigger_migrate(request):
    call_command('migrate')
    return HttpResponse("Migration done.")

def trigger_collectstatic(request):
    call_command('collectstatic', interactive=False)
    return HttpResponse("Collectstatic done.")

urlpatterns += [
    path('run-migrate/', trigger_migrate),
    path('run-collectstatic/', trigger_collectstatic),
]
