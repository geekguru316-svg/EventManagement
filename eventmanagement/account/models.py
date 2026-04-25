from django.db import models
from django.contrib.auth.hashers import check_password, identify_hasher, make_password

class Account(models.Model):

    USER_TYPE = (
        ('A', 'Admin'),
        ('S', 'Student'),
        ('T', 'Teacher'),
    )

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50)

    type = models.CharField(max_length=1, choices=USER_TYPE)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        try:
            identify_hasher(self.password)
            return check_password(raw_password, self.password)
        except Exception:
            return self.password == raw_password
