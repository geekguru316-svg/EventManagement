from django.db import models
from account.models import Account
from event.models import Event

class Student(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    course = models.CharField(max_length=100)
    year = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.account.username


class AttendEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    status = models.CharField(max_length=20)
    date_registered = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.event}"