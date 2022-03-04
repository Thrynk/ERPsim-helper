from django.contrib import admin
from django.db import models

from django.db import models


class Contact(models.Model):
    gameNumber = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
