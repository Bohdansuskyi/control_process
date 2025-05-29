from django.db import models

class station(models.Model):
    name = models.CharField(max_length=50)
    MLX90614_adress = models.CharField(max_length=6)
    RFID_adress = models.CharField(max_length=6)
    station_identification_number = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)


class parts(models.Model):
    UID = models.CharField(max_length=20)
    EEPROM_description = models.TextField()
    part_identification_number = models.PositiveIntegerField(default=0)


class records(models.Model):
    station = models.ForeignKey(station,on_delete=models.CASCADE)
    part = models.ForeignKey(parts,on_delete=models.CASCADE)
    temperature = models.FloatField()
    time = models.TimeField(auto_now=False,auto_now_add=False)
    Date = models.DateField(auto_now=False, auto_now_add=False)