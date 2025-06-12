from django.shortcuts import render
from .models import parts, records, station
from django.db.models import Max
from datetime import date, timedelta
from .forms import UIDSearchForm
from django.contrib import messages


#django rest_framework (API)
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import StationSerializer,RecordsSerializer
from rest_framework.views import APIView
from datetime import datetime

def index(request):
    return render(request,"app/index.html")

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

# API

class StationListCreate(generics.ListCreateAPIView):
    queryset = station.objects.all()
    serializer_class = StationSerializer

class StationCreateView(APIView):
    # GET get the parameters from the URL
    def get(self,request):
        MLX90614_adress = request.GET.get('MLX90614_adress')
        RFID_adress = request.GET.get('RFID_adress')

        if MLX90614_adress and RFID_adress:
            # Logic for data processing
            station_data = {
                'MLX90614_adress':MLX90614_adress,
                'RFID_adress':RFID_adress
            }

            serializer = StationSerializer(data=station_data)

            if serializer.is_valid():
                serializer.save() # Save the data to the database
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"error":"MLX90614_adress and RFID_adress are required."},status=status.HTTP_400_BAD_REQUEST)
    

class RecordsListCreate(generics.ListCreateAPIView):
    queryset = records.objects.all()
    serializer_class = RecordsSerializer


class RecordsCreateView(APIView):
    def get(self, request):
        mlx_adress = request.GET.get('MLX90614_adress')  # zamiast nazwy stacji
        part_uid = request.GET.get('part')
        temperature = request.GET.get('temperature')

        if not (mlx_adress and part_uid and temperature):
            return Response(
                {"error": "Wymagane pola: MLX90614_adress, part (UID), temperature"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # SZUKANIE STACJI PO ADRESIE MLX90614
        try:
            station_obj = station.objects.get(MLX90614_adress=mlx_adress)
        except station.DoesNotExist:
            return Response(
                {"error": f"Stacja z adresem MLX90614 '{mlx_adress}' nie istnieje"},
                status=status.HTTP_404_NOT_FOUND
            )

        # PRÓBA POBRANIA ISTNIEJĄCEJ CZĘŚCI
        part_obj = parts.objects.filter(UID=part_uid).first()

        if part_obj is None:
            # OBLICZAMY KOLEJNY NUMER IDENTYFIKACYJNY
            # szukanie ostatniego numeru identyfikacyjnego
            last_number = parts.objects.aggregate(Max('part_identification_number'))['part_identification_number__max'] or 0

            new_number = last_number + 1

            part_obj = parts.objects.create(
                UID=part_uid,
                EEPROM_description='',
                part_identification_number=new_number
            )

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
