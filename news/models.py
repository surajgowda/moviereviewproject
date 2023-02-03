from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.headline

# Create your models here.
