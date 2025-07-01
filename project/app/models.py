from django.db import models

class station(models.Model):
    name = models.CharField(max_length=50)
    MLX90614_adress = models.CharField(max_length=6)

    def __str__(self):
        return f"Stancja:{self.name}  MLX90614:{self.MLX90614_adress}"


class parts(models.Model):
    UID = models.CharField(max_length=20)
    EEPROM_description = models.TextField()
    part_identification_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Numer detalu:{self.part_identification_number}  UID:{self.UID}"


class records(models.Model):
    station = models.ForeignKey(station,on_delete=models.CASCADE)
    part = models.ForeignKey(parts,on_delete=models.CASCADE)
    temperature = models.FloatField()
    time = models.TimeField(auto_now=False,auto_now_add=False)
    Date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"Stancja:{self.station}  Detal:{self.part}  Temperatura{self.temperature}  Czas:{self.time}  Data:{self.Date}"