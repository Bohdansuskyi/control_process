from django.shortcuts import render
from .models import parts, records, station
from datetime import date, timedelta


#django rest_framework (API)
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import StationSerializer,RecordsSerializer
from rest_framework.views import APIView
from datetime import datetime

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
        station_name = request.GET.get('station')
        part_uid = request.GET.get('part')
        temperature = request.GET.get('temperature')

        if station_name and part_uid and temperature:
            station_obj, _ = station.objects.get_or_create(
                name=station_name,
                defaults={
                    'MLX90614_adress': '000000',
                    'RFID_adress': '000000',
                    'station_identification_number': 0,
                    'is_active': False
                }
            )

            part_obj, _ = parts.objects.get_or_create(
                UID=part_uid,
                defaults={
                    'EEPROM_description': '',
                    'part_identification_number': 0
                }
            )

            now = datetime.now()

            record_data = {
                'station': station_obj.id,
                'part': part_obj.id,
                'temperature': temperature,
                'time': now.strftime("%H:%M:%S"),     # tutaj string
                'Date': now.strftime("%Y-%m-%d"),     # i tu też
            }

            serializer = RecordsSerializer(data=record_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Wymagane pola: station (name), part (UID), temperature"}, status=status.HTTP_400_BAD_REQUEST)