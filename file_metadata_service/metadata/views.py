from rest_framework import generics
from .models import FileMetadata
from .serializers import FileMetadataSerializer


class FileMetadataListCreate(generics.ListCreateAPIView):
    queryset = FileMetadata.objects.all()
    serializer_class = FileMetadataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        file_type = self.request.query_params.get('file_type')
        min_size = self.request.query_params.get('min_size')
        max_size = self.request.query_params.get('max_size')
        equal_size = self.request.query_params.get('equal_size')

# TODO: add filter validation logic somewhere
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        if min_size:
            queryset = queryset.filter(file_size__gte=min_size)
        if max_size:
            queryset = queryset.filter(file_size__lte=max_size)
        if equal_size:
            queryset = queryset.filter(file_size=equal_size)

        return queryset
