from django.db import models
from account.models import Account

class Teacher(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    specialization = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.account.username