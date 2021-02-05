from django.db import models

class GameTypes(models.Model):

    label = models.CharField(max_length=50)