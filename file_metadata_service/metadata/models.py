from django.db import models


class FileMetadata(models.Model):
    file_url = models.TextField(unique=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_url
