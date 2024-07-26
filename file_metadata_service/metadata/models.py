from django.db import models, connection
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class FileMetadata(models.Model):
    file_url = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["file_size"]),
            models.Index(fields=["file_type"]),
            models.Index(fields=["file_name"]),
        ]


# Signal to check and create the table if it doesn't exist
@receiver(post_migrate)
def ensure_file_metadata_table_exists(sender, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE SEQUENCE IF NOT EXISTS file_metadata_seq START WITH 1 INCREMENT BY 1;
            CREATE TABLE IF NOT EXISTS file_metadata (
                id BIGSERIAL PRIMARY KEY DEFAULT nextval('file_metadata_seq'),
                file_url VARCHAR(1024) NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_type VARCHAR(50) NOT NULL,
                file_size BIGINT NOT NULL,
                upload_date TIMESTAMP WITHOUT TIME ZONE NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_file_size ON file_metadata(file_size);
            CREATE INDEX IF NOT EXISTS idx_file_type ON file_metadata(file_type);
            CREATE INDEX IF NOT EXISTS idx_file_name ON file_metadata(file_name);
        """
        )
