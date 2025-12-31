from dataclasses import dataclass
from pathlib import Path
from typing import overload
import requests
import logging
import re

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


@dataclass
class BookURL:
    name: str
    download_url: str


@dataclass
class RegexMatch:
    book_name: str
    context: str


@dataclass
class SearchResults:
    total_matches: int
    first_match_idx: int
    matches: list[RegexMatch]


class Library:
    book_urls = [
        BookURL(
            name="Moby Dick",
            download_url="https://www.gutenberg.org/ebooks/2701.txt.utf-8",
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
    searches_cache = {}

    cache_dir = Path(__file__).parent / "books_cache"

    def __init__(self):
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def list_books(self) -> list[str]:
        return [book.name for book in self.book_urls]

    @overload
    def get_content(self, book_name: str) -> str: ...

    def get_content(self, book: BookURL) -> str:
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

    def get_lenght(self, book_name: str):
        book_content = self.get_content(book_name)
        return len(book_content)

    def regex_search(
        self,
        book_name: str,
        regex: str,
        context_size: int = 100,
    ) -> list[RegexMatch]:
        book_content = self.get_content(book_name)
        key = (book_name, regex)
        if key not in self.searches_cache:
            self.searches_cache[key] = []
            breakpoint()
            for match in re.finditer(regex, book_content):
                context_start = max(0, match.start() - context_size)
                context_end = min(
                    len(book_content),
                    match.end() + context_size
                )
                self.searches_cache[key].append(
                    RegexMatch(
                        book_name,
                        book_content[context_start: context_end],
                    )
                )
        return self.searches_cache[key]

    def paginated_regex_search(
        self,
        book_name: str,
        regex: str,
        context_size: int = 100,
        page_idx: int = 0,
        page_size: int = 10,
    ) -> SearchResults:
        matches = self.regex_search(book_name, regex, context_size)
        first_match_idx = page_idx * page_size
        return SearchResults(
            total_matches=len(matches),
            first_match_idx=first_match_idx,
            matches=matches[first_match_idx: first_match_idx + page_size],
        )
