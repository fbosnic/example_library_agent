from library_agent.library import Library


def test_book_download():
    library = Library()
    book_content = library.download_book("Moby Dick")
    print(book_content)


if __name__ == "__main__":
    test_book_download()
