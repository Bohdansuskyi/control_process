from django.shortcuts import render
from .models import records, station

def index(request):
    return render(request,"app/index.html")

def info(request):
    return render(request,"app/info.html")


def charts(request):
    # Pobranie wszystkich rekordów posortowanych po stacji i czasie
    data = records.objects.all().order_by('station__id', '-time')

    # Tworzenie słownika, gdzie klucz to nazwa stacji, a wartość to dane tej stacji
    station_data = {}

    for entry in data:
        station_name = entry.station.name
        if station_name not in station_data:
            station_data[station_name] = {
                'times': [],
                'temperatures': []
            }
        station_data[station_name]['times'].append(str(entry.time))
        station_data[station_name]['temperatures'].append(entry.temperature)

    return render(request, "app/charts.html", {
        'station_data': station_data
    })