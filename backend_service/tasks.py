from app.celery import app
from backend_service.services.photos import AlbumsFetchTask
from backend_service.utils.multithreading import Pool


@app.task
def albums_fetcher_task():
    service = AlbumsFetchTask(Pool())

    service.fetch_albums()
    service.fetch_photos()

    return
