import argparse

from django.core.management import BaseCommand

from backend_service.services.photos import AlbumsFetchTask
from backend_service.utils.multithreading import Pool


class Command(BaseCommand):

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--threads', type=int)
        parser.add_argument('--chunk_size', type=int)

    def handle(self, *args, **options):
        pool = Pool(threads=options.get('threads'), chunk_size=options.get('chunk_size'))

        service = AlbumsFetchTask(pool)
        service.fetch_albums()
        service.fetch_photos()
