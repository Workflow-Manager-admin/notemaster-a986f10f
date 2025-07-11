from django.db import models
from django.conf import settings

# PUBLIC_INTERFACE
class Note(models.Model):
    """
    Represents a note owned by a user.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title
