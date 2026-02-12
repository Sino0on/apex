from django.db import models


class University(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='university_logos/')
    image = models.ImageField(upload_to='university_images/', blank=True, null=True)
    description = models.TextField()
    mini_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'
        ordering = ['-updated_at']