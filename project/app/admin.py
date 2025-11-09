from django.contrib import admin
from .models import station,parts,records

# zarejestruje model w panelu administracyjnym
admin.site.register(station)
admin.site.register(parts)
admin.site.register(records)
