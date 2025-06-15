from rest_framework import serializers
from .models import records

# convert data from json to float, string, ..



class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = records
        fields = '__all__'