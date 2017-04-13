from django.db import models
# Create your models here.
# class Candidate(models.Model):
#     name = models.CharField(max_length=10)
#     introduction = models.TextField()
#     party_number = models.IntegerField(default=0)
#     def __str__(self):
#         return self.name

class Card_Text(models.Model):
    introduction = models.TextField()
    def __str__(self):
         return self.introduction