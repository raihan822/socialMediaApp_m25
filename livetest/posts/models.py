from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New field for media type tracking
    MEDIA_TYPE_CHOICES = [
        ('text', 'Text Only'),
        ('image', 'Image'),
    ]
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='text'
    )

    def save(self, *args, **kwargs):
        """Automatically set media type on save"""
        self.media_type = 'image' if self.image else 'text'
        super().save(*args, **kwargs)