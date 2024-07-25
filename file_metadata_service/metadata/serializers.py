from urllib.parse import urlparse
from rest_framework import serializers
from .models import FileMetadata
from minio import Minio
from minio.error import S3Error


class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = ['file_url']

    def create(self, validated_data):
        # Here we'll extract metadata from MinIO
        file_url = validated_data.get('file_url')
        file_type, file_size, file_name, file_url_clean = get_metadata_from_minio(file_url)

        file_metadata = FileMetadata(
            file_url=file_url_clean,
            file_type=file_type,
            file_size=file_size,
            file_name=file_name,
        )
        file_metadata.save()
        return file_metadata


def get_metadata_from_minio(file_url):
    # Validate the URL
    if not validate_url(file_url):
        raise serializers.ValidationError("Invalid file URL")

    # TODO: This is a placeholder; replace with actual MinIO interaction
    # TODO: add validations for url, size, etc
    # TODO: move credentials to settings
    minio_client = Minio(
        'minio.example.com',
        access_key='minioadmin',
        secret_key='minioadmin',
        secure=True
    )

    try:
        # Extract bucket and object name from URL
        bucket_name, object_name = extract_bucket_and_object(file_url)

        # Get object stats
        stat = minio_client.stat_object(bucket_name, object_name)

        file_type = stat.content_type
        file_size = stat.size
        file_name = file_url.split('/')[-1]
        file_url_clean = file_url.split('?')[0]

        # Additional validations
        if file_size <= 0:
            raise serializers.ValidationError("File size must be greater than zero")
        if not file_type:
            file_type = 'application/octet-stream'  # Default type if not provided

        return file_type, file_size, file_name, file_url_clean
    except S3Error as err:
        raise serializers.ValidationError(f'Error retrieving metadata: {str(err)}')

def extract_bucket_and_object(file_url):
    # Logic to extract bucket and object name from the URL
    # TODO: Example placeholder; adjust according to your URL structure
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.lstrip('/').split('/')
    bucket_name = path_parts[0]
    object_name = '/'.join(path_parts[1:])
    return bucket_name, object_name

def validate_url(file_url):
    parsed_url = urlparse(file_url)
    return all([parsed_url.scheme, parsed_url.netloc, parsed_url.path])
