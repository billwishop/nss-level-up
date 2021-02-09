from django.db import models

class Event(models.Model):

    event_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    scheduler = models.ForeignKey("Gamer", on_delete=models.CASCADE)