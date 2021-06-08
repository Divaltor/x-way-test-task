from rest_framework import serializers

from backend_service.models import Album, Photo


class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Album
        fields = ['id', 'title']


class PhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    album_id = serializers.IntegerField(write_only=True)
    url = serializers.URLField()
    thumbnail_url = serializers.URLField()

    class Meta:
        model = Photo
        fields = ['id', 'title', 'url', 'thumbnail_url', 'album_id']


class AlbumWithPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'photos']
