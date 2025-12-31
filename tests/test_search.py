from library_agent.library import Library


def test_search_content():
    library = Library()
    search_results = library.paginated_regex_search(
        "Moby Dick", r"whale", context_size=100, page_idx=0, page_size=10
    )
    print(search_results)


if __name__ == "__main__":
    test_search_content()
