from django.shortcuts import render, redirect, get_object_or_404
from .models import parts, records, station
from django.db.models import Max
from datetime import date, timedelta
from .forms import UIDSearchForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import make_aware
from .forms import TemperatureThresholdForm

# django rest_framework (API)
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RecordsSerializer
from rest_framework.views import APIView
from datetime import datetime

new_data_flag = False

# deklaracja widoku który podaje pomiary z progami temperatur
def index(request):
    form = TemperatureThresholdForm(request.GET or None)
    max_temp = None
    min_temp = None
    history_in_range = []
    history_out_range = []

    # walidacja zadanych temperatur
    if form.is_valid():
        max_temp = form.cleaned_data['max_temp']
        min_temp = form.cleaned_data['min_temp']

        if min_temp >= max_temp:
            messages.error(request, "Dolny próg musi być mniejszy od górnego.")
        else:
            history_in_range = records.objects.filter(
                temperature__gte=min_temp,
                temperature__lte=max_temp
            ).order_by("Date", "time")

            history_out_range = records.objects.exclude(
                temperature__gte=min_temp,
                temperature__lte=max_temp
            ).order_by("Date", "time")

            if not history_in_range:
                messages.warning(request, "Brak danych w podanym zakresie temperatur.")
            else:
                messages.success(
                    request,
                    f"Znaleziono {history_in_range.count()} rekordów w zakresie {min_temp}℃ - {max_temp}℃"
                )

    return render(request, "app/index.html", {
        'form': form,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'history_in_range': history_in_range,
        'history_out_range': history_out_range,
    })

# deklaracja widoku z wyszukiwarką dla konkretnego detalu
def info(request):
    form = UIDSearchForm(request.GET or None)
    history = []
    part_obj = None

    if form.is_valid():
        uid = form.cleaned_data['uid']
        try:
            part_obj = parts.objects.get(UID=uid)
            history = records.objects.filter(part=part_obj).order_by("Date", "time")

            if not history:
                messages.warning(request, "Brak danych historycznych dla tego detalu.")

        except parts.DoesNotExist:
            part_obj = None
            messages.error(request, "Nie znaleziono detalu o takim UID.")

    return render(request, "app/info.html", {
        'form': form,
        'part': part_obj,
        'history': history,
    })
# Sprawdza, czy pojawiły się nowe dane do odświeżenia strony
def check_data_update(request):
    global new_data_flag
    response = {'new': new_data_flag}
    new_data_flag = False  # resetujemy flagę po odczytaniu
    return JsonResponse(response)

# deklaracja widoku z wykresami
def charts(request):
    date_filter = request.GET.get('filter', 'all')

    queryset = records.objects.all()
    # filter
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

## API

    
# lista wszystkich rekordów dla rekordów
class RecordsListCreate(generics.ListCreateAPIView):
    queryset = records.objects.all()
    serializer_class = RecordsSerializer

# punkt końcowy w API dla rekordów
class RecordsCreateView(APIView):
    def get(self, request):
        global new_data_flag
        mlx_adress = request.GET.get('MLX90614_adress')  
        part_uid = request.GET.get('part')
        temperature = request.GET.get('temperature')

        if not (mlx_adress and part_uid and temperature):
            return Response(
                {"error": "Wymagane pola: MLX90614_adress, part (UID), temperature"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # wyszukiwanie stacji według adresu MLX90614
        try:
            station_obj = station.objects.get(MLX90614_adress=mlx_adress)
        except station.DoesNotExist:
            return Response(
                {"error": f"Stacja z adresem MLX90614 '{mlx_adress}' nie istnieje"},
                status=status.HTTP_404_NOT_FOUND
            )

        # pobiera dane o istniejących częściach
        part_obj = parts.objects.filter(UID=part_uid).first()

        if part_obj is None:
            # jeśli nie ma takiej części, dodaje nową ze zmienionym numerem identyfikacyjnym części
            last_number = parts.objects.aggregate(Max('part_identification_number'))['part_identification_number__max'] or 0

            new_number = last_number + 1

            part_obj = parts.objects.create(
                UID=part_uid,
                EEPROM_description='',
                part_identification_number=new_number
            )

        # pobiera aktualny czas w momencie przypisywania danych do bazy danych
        now = datetime.now()

        record_data = {
            'station': station_obj.id,
            'part': part_obj.id,
            'temperature': temperature,
            'time': now.strftime("%H:%M:%S"),
            'Date': now.strftime("%Y-%m-%d"),
        }

        serializer = RecordsSerializer(data=record_data)

        if serializer.is_valid():
            serializer.save()
            new_data_flag = True
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

