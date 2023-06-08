from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
class Makesentence(models.Model):
    created_at = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    word = models.TextField(default="", unique=False, max_length=255)
    sentence = models.TextField(default="", unique=False, max_length=255)
    meaning = models.TextField(default="", unique=False, max_length=255)
    
    class Meta:
        ordering = ["-id"]
        
    def __str__(self):
        return self.sentence
    
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(null=True, unique=False)
 