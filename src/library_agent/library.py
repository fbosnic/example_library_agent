from dataclasses import dataclass
from pathlib import Path
from typing import overload
import requests
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


@dataclass
class BookURL:
    name: str
    download_url: str


class Library:
    book_urls = [
        BookURL(
            name="Moby Dick",
            download_url="https://www.gutenberg.org/ebooks/1342.txt.utf-8",
        ),
        BookURL(
            name="Frankenstein",
            download_url="https://www.gutenberg.org/ebooks/84.txt.utf-8",
        ),
        BookURL(
            name="Pride and Prejudice",
            download_url="https://www.gutenberg.org/ebooks/1342.txt.utf-8",
        ),
    ]

    cache_dir = Path(__file__).parent / "books_cache"

    def __init__(self):
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def list_books(self):
        return [book.name for book in self.book_urls]

    @overload
    def download_book(self, book_name: str) -> str: ...

    def download_book(self, book: BookURL) -> str:
        if isinstance(book, str):
            try:
                book = next(filter(lambda b: b.name == book, self.book_urls))
            except StopIteration:
                raise ValueError(f"Book {book} not found")

        book_path = self.cache_dir / f"{book.name}.txt"
        if book_path.exists():
            return book_path.read_text()
        else:
            LOGGER.info(f"Downloading {book.name}...")
            response = requests.get(book.download_url)
            book_path.write_text(response.text)
            return response.text
