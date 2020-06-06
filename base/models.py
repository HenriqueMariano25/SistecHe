from django.db import models
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=200)
    admission_date = models.DateField()
    demission_date = models.DateField(blank=True, null=True)
    leader = models.BooleanField(default=False)
    leader_name = models.CharField(max_length=200)
    manager = models.CharField(max_length=200)
    registration = models.IntegerField()
    occupation = models.CharField(max_length=200)
    extra_hour = models.FloatField(blank=True, null=True, default=0.0)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, blank=True, null=True)
    sub_sector = models.ForeignKey(SubSector, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ImportHistory(models.Model):
    type = models.CharField(max_length=50)
    made_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.CharField(max_length=50)


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration = models.IntegerField()
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, blank=True, null=True)
    permission = models.IntegerField()

    def __str__(self):
        return self.user.username


class ReleasedHour(models.Model):
    released_hour = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='releasedhours')
    reason = models.CharField(max_length=150)
    made_by = models.CharField(max_length=150)
    create_at = models.DateTimeField()


class LimitHour(models.Model):
    hours = models.FloatField()
    made_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField()


class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    final_time = models.TimeField()
    duration = models.FloatField()

class Scheduling(models.Model):
    date = models.DateField(null=False,blank=False)
    reason = models.CharField(max_length=200,null=False,blank=False)
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)

class Emplo_Schedu(models.Model):
    employee = models.ForeignKey(User, on_delete=models.PROTECT)
    scheduling = models.ForeignKey(Scheduling, on_delete=models.PROTECT)
    plus_he = models.FloatField(default=0.0)