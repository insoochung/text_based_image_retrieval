from django.db import models

# Create your models here.
class Photo(models.Model):
    image_path = models.ImageField(upload_to='photos')
    caption = models.CharField(max_length=255)
    caption_vector = models.JSONField(null=True, blank=True)
    names = models.CharField(max_length=255)
    name_vector = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.caption
