from django.db import models

# Create your models here.
class Cardnews(models.Model):
    # _id = models.IntegerField(primary_key=True) -> id필드 자동생성됨
    tendency = models.IntegerField(default=1)
    title = models.CharField(max_length=50)
    target = models.CharField(max_length=30)
    article = models.TextField()
    articleUrl = models.URLField(max_length=200)
    publish_time = models.DateTimeField(auto_now_add=False)
    collecting_time = models.DateTimeField(auto_now_add=True)
    # publish_time = models.DateField(auto_now=False)
    # collecting_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title