from django.db import models

# Create your models here.

class Image(models.Model):
    photo = models.ImageField(upload_to='uploads/')
    title = models.CharField(max_length=200, null=False)
    desc = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title