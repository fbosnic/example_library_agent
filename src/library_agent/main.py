from library_agent.library import Library
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import AIMessage
from langchain_ollama import ChatOllama


SYSTEM_PROMPT = """
You are a helpful library assistant that can provide information on books.
At your disposal you have various tools that you should use to answer
the questions. Do not make up answers or informations that

"""


def main():
    library = Library()

    @tool
    def list_books():
        """Lists books abailable in the library.

        Use this tool to find the exact name of the books in the library.
        """
        return library.list_books()

    @tool
    def regex_search_book_paginated(
        book_name: str,
        regex: str,
        page_idx: int = 0,
    ) -> list[str]:
        """Searches for matches for a given regex in a book.

        ## Notes
        - This is a great tool to find information within a book.
            This function will always return a page of 10 results. If you
            want to see more results, you can use the page_idx parameter
            to get the next page of results.
        - Make sure that the name of the book is correctly spelled.
            Otherwise, the toll will return an error.

        ## Example
        Suppose that the user would like to know what color the hair
        of Harry Potter is:
        1) First, check whether Harry Potter books are in the library
        2) Use this tool to search for "Harry Potter" in any of these
        books and get books snippets
        3) Check the snippets for the hair color.

        """
        try:
            search_results = library.paginated_regex_search(
                book_name,
                regex,
                page_idx=page_idx
            )
            return [match.context for match in search_results.matches]
        except ValueError as ex:
            return f"Error: {ex}"

    llm = ChatOllama(
        model="llama3.3",
        temperature=0.1,
        base_url="http://192.168.88.15:11434",
        tools=[library.list_books],
    )
    agent = create_agent(
        model=llm,
        system_prompt=(
            "You are a helpful library assistant that can provide information on books."
            " At your disposal you have various different tools that you can use to find"
            " the information you need for answering questions."
            " Do not make up information that you can not find using your tools."
            " If you are not sure about the answer, say that you do not know."
        ),
        tools=[list_books, regex_search_book_paginated],
    )

    context = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "Can you describe captain Ahab?"}
            ]
        },
        print_mode="messages",
    )

    for msg in context["messages"]:
        if isinstance(msg, AIMessage):
            print(msg.content)


if __name__ == "__main__":
    main()
