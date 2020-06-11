from django.db import models
from django.contrib.auth.models import User


# Create your models here.w
class SubSector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'name': self.name,
        }


class Sector(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def to_json(self):
        return {'name': self.name,'id': self.id}


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

    def to_json(self):
        if self.sector is None:
            self.sector = 0
        return {
            'name': self.name,
            'admission_date': self.admission_date,
            'demission_date': self.demission_date,
            'leader': self.leader,
            'leader_name': self.leader_name,
            'manager': self.manager,
            'registration': self.registration,
            'occupation': self.occupation,
            'extra_hour': self.extra_hour,
            'sector': self.sector.to_json(),
            'sub_sector': self.sub_sector.to_json(),
        }


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

    def to_json(self):
        return {
            'name': self.name,
            'star_time': self.start_time,
            'final_time': self.final_time,
            'duration': self.duration,
            'id': self.id,
        }


class Scheduling(models.Model):
    date = models.DateField(null=False, blank=False)
    reason = models.CharField(max_length=200, null=False, blank=False)
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)

    def to_json(self):
        return {
            'id': self.id,
            'date': self.date,
            'reason': self.reason,
            'shift': self.shift.to_json(),
            # 'user': self.user.to_json(),
            'sector': self.sector.to_json()
        }


class Emplo_Schedu(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    scheduling = models.ForeignKey(Scheduling, on_delete=models.PROTECT)
    plus_he = models.FloatField(default=0.0)

    def to_json(self):
        return {
            'id': self.id,
            'employee': self.employee.to_json(),
            'scheduling': self.scheduling.to_json(),
            'plus_he': self.plus_he
        }
