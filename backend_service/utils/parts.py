import math
import os
from typing import Iterable


def paginate(data: Iterable, page: int = 0, limit: int = 10) -> Iterable:
    return data[page * limit:page * limit + limit]


def get_optimal_cpu_count():
    return (os.cpu_count() or 4) * 4


def split_by_chunks(iterable: list, chunk_size: int) -> list[Iterable]:
    pages_count = math.ceil(len(iterable) / chunk_size)

    chunks = []

    for page in range(pages_count):
        chunk = paginate(iterable, page, chunk_size)

        chunks.append(chunk)

    return chunks