from datetime import datetime
from django.utils.timezone import make_aware
from .models import records

# Funkcja pobiera ostatni rekord z bazy danych, łączy jego datę i czas w jeden obiekt datetime, 
# aby określić moment ostatniej aktywności
def last_activity_context(request):
    last_activity = None
    last_record = records.objects.last()
    if last_record:
        dt = datetime.combine(last_record.Date, last_record.time)
        last_activity = make_aware(dt)
    return {
        "last_activity": last_activity
    }
