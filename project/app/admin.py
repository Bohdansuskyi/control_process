from django.contrib import admin
from .models import station,parts,records

# register model in admin panel
admin.site.register(station)
admin.site.register(parts)
admin.site.register(records)
