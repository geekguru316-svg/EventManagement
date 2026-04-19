from django.db import models

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return self.room_name
