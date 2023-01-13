from django.db import models

# Create your models here.


class Antenna(models.Model):
    x_localization = models.IntegerField()
    y_localization = models.IntegerField()
    name = models.CharField(max_length=30)


class Message(models.Model):
    antenna = models.ForeignKey(Antenna, on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    distance = models.IntegerField()
    created_at = models.DateTimeField()


