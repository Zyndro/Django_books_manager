from django.db import models

# Create your models here.

class Books(models.Model):

    def __str__(self):
        return ("Title: " + self.title +" Author: "+self.authors)
    title = models.CharField(max_length=256)
    authors = models.CharField(max_length=256)
    publishedDate = models.CharField(max_length=20, default=1900)
    industryIdentifiers = models.CharField(max_length=256)
    pageCount = models.IntegerField(default=0)
    imageLinks = models.CharField(max_length=1024)
    language = models.CharField(max_length=10)


