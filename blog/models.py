from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)


    def __str__(self):
        return self.title



    class Meta:
        ordering = ('-date_published',)