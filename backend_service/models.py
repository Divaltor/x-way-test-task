from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token


class Album(models.Model):
    title = models.CharField(max_length=255)


# Не использую URLField в url и thumbnail_url,
# потому что в теории ссылка на изображение может быть больше лимита в 255 символов (URLField наследуется от CharField)
class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.TextField(max_length=None)
    thumbnail_url = models.TextField(max_length=None)
    extension = models.CharField(max_length=32, default='jpeg')
    file = models.FileField(blank=True, null=True, upload_to='images/%Y-%m-%d')
