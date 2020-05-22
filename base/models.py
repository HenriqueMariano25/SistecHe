from django.db import models


# Create your models here.
class SubSector(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    cpf = models.IntegerField()
    admission_date = models.DateField()
    demission_date = models.DateField()
    leader = models.BooleanField()
    leader_name = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    registration = models.IntegerField()
    occupation = models.CharField(max_length=100)
    extra_hour = models.FloatField()
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    sub_sector = models.ForeignKey(SubSector, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
