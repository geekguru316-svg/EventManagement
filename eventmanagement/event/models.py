from django.db import models
from teacher.models import Teacher
from room.models import Room

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)

    event_title = models.CharField(max_length=200)
    date_of_event = models.DateField()
    max_participants = models.IntegerField()

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_title