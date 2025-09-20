from datetime import datetime
from django.utils.timezone import make_aware
from .models import records

def last_activity_context(request):
    last_activity = None
    last_record = records.objects.last()
    if last_record:
        dt = datetime.combine(last_record.Date, last_record.time)
        last_activity = make_aware(dt)
    return {
        "last_activity": last_activity
    }
