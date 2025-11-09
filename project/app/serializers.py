from rest_framework import serializers
from .models import records

# konwertuje dane z formatu json na formarty czytelne dla aplikacji



class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = records
        fields = '__all__'