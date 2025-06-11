from django.shortcuts import render
from .models import records, station
from datetime import date, timedelta


def index(request):
    return render(request,"app/index.html")

def info(request):
    return render(request,"app/info.html")


def charts(request):
    date_filter = request.GET.get('filter', 'all')

    queryset = records.objects.all()

    if date_filter == 'today':
        queryset = queryset.filter(Date=date.today())
    elif date_filter == 'yesterday':
        queryset = queryset.filter(Date=date.today() - timedelta(days=1))

    data = queryset.order_by('station__id', 'Date', 'time')

    station_data = {}
    for entry in data:
        station_name = entry.station.name
        if station_name not in station_data:
            station_data[station_name] = {
                'times': [],
                'temperatures': []
            }
        datetime_str = f"{entry.Date} {entry.time}"
        station_data[station_name]['times'].append(datetime_str)
        station_data[station_name]['temperatures'].append(entry.temperature)

    return render(request, "app/charts.html", {
        'station_data': station_data,
        'selected_filter': date_filter
    })