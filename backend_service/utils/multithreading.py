from typing import Callable, Iterator, TypeVar, Iterable

import concurrent.futures

from loguru import logger

from backend_service.utils.parts import get_optimal_cpu_count, split_by_chunks

_T = TypeVar('_T')


class Pool:

    def __init__(self, threads: int = None, chunk_size: int = None):
        self.threads = threads or get_optimal_cpu_count()
        self.chunk_size = chunk_size or 150

    def send_to_pool(self, data: list[list], func: Callable, *args, **kwargs) -> Iterator[_T]:

        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as pool:
            for chunk in split_by_chunks(data, self.chunk_size):
                futures.append(pool.submit(func, chunk, *args, **kwargs))

        return futures
