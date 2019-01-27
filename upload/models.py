from django.db import models

# Create your models here.

class Image(models.Model):
    photo = models.ImageField(blank=False, upload_to='uploads/', null=False)
    title = models.CharField(max_length=20)
    remarks = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title