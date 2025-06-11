from rest_framework import serializers
from .models import station,parts,records

# convert data from json to float, ...

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = station
        fields = ["MLX90614_adress","RFID_adress"]


class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = records
        fields = '__all__'