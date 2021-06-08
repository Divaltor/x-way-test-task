import concurrent.futures
import pathlib
import re
from io import BytesIO
from typing import Union
from uuid import uuid4

import PIL.Image
import httpx
from PIL import Image as PILImage
from any_case import converts_keys
from django.core.files.base import ContentFile
from django.db import transaction
from loguru import logger
from rest_framework.exceptions import ValidationError

from backend_service.models import Photo, Album
from backend_service.serializers import PhotoSerializer, AlbumSerializer
from backend_service.services.http_client import HTTPClient
from backend_service.utils.multithreading import Pool

URL_SIZE_PATTERN = re.compile(r'(?P<domain>\.\w+/)\d+', re.I)


def replace_image_url_to_higher_size(url: str, size: Union[int, str] = 1000) -> str:
    return re.sub(URL_SIZE_PATTERN, f"\g<domain>{size}", url)


# В идеале поменять бы на какой-нибудь класс или что-то такое и добавить параметры куда сохранять
def process_photos(photos: list[Photo]) -> list[Photo]:
    logger.debug(len(photos))
    for photo in photos:
        url = replace_image_url_to_higher_size(photo.url)
        response = httpx.get(url, timeout=5)

        if response.is_error:
            logger.warning(f'Failed to download image {photo.title} from album ID: {photo.album}')
            continue

        image = Image(BytesIO(response.read()))
        # В идеале это как-то сделать опциональным для функции или пачки
        # Чтобы можно было указывать в какой размер конвертировать
        image.resize(width=500, height=500)

        uuid = str(uuid4())

        photo.file.save(f'{photo.title}-{uuid}.{photo.extension}', ContentFile(image.get_file_object()), save=False)

    return photos


class Image:
    def __init__(self, image_path: Union[str, pathlib.Path, BytesIO]):
        self._image_path = image_path

        self.image: PIL.Image.Image = PILImage.open(self._image_path)

    def resize(self, width: int, height: int) -> None:
        self.image = self.image.resize((width, height), PILImage.ANTIALIAS)

    def get_file_object(self) -> bytes:
        bytes_io = BytesIO()
        self.image.convert('RGB').save(bytes_io, format='JPEG')
        return bytes_io.getvalue()


class ApiFetchException(Exception):
    pass


# TODO: Можно разделить на два отдельных класса и вызывать через фабрику
class FetcherService:

    def __init__(self):
        self.client = HTTPClient('https://jsonplaceholder.typicode.com')

    def get_photos(self) -> PhotoSerializer:
        response = self.client.get('/photos')

        if response.is_error:
            raise ApiFetchException('Can\'t get photos')

        photos = PhotoSerializer(data=converts_keys(response.json()), many=True)

        if not photos.is_valid():
            raise ValidationError()

        return photos

    def get_albums(self) -> AlbumSerializer:
        response = self.client.get('/albums')

        if response.is_error:
            raise ApiFetchException('Can\'t get albums')

        albums = AlbumSerializer(data=converts_keys(response.json()), many=True)

        if not albums.is_valid():
            raise ValidationError()

        return albums


class AlbumsFetchTask:

    def __init__(self, pool: Pool):
        self.service = FetcherService()
        self.pool = pool

    def fetch_photos(self) -> list[Photo]:
        photos = self.service.get_photos()

        models = [Photo(**item) for item in photos.validated_data]

        results = []

        futures = self.pool.send_to_pool(models, process_photos)

        with transaction.atomic():
            for task in concurrent.futures.as_completed(futures):
                try:
                    result: list[Photo] = task.result()

                    # Если album_id is None, то необходимо подумать насчет вторичного ключа
                    # И как проверять наличие ключа без ущерба скорости базы
                    results.extend(Photo.objects.bulk_create(result))
                except Exception as ex:
                    logger.exception(ex)

        logger.debug(results)
        return results

    def fetch_albums(self) -> list[Album]:
        albums = self.service.get_albums()

        with transaction.atomic():
            return [Album.objects.update_or_create(**item) for item in albums.validated_data]
