from django.db import models

# Create your models here.
# class News(models.Model):
#     tendency = models.CharField(max_length=20)
#     keyword = models.CharField(max_length=20)
#     article = models.TextField()
#     # publish_time = models.DateTimeField(auto_now_add=False)
#     publish_time = models.DateTimeField(auto_now_add=True)

class cardnews(models.Model):
    title = models.CharField(max_length=100)
    article = models.TextField()
    imgUrl = models.CharField(max_length=200)
    # img = models.ImageField(upload_to='cardnews/static/img',null=True)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.imgUrl