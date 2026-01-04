from library_agent.library import Library
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import AIMessage
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

import dotenv
import os


dotenv.load_dotenv()


SYSTEM_PROMPT = """
You are a helpful library assistant that can provide information on books.
At your disposal you have various tools that you should use to answer
the questions.

## Answering questions and requests
When answering, follow these steps:
1) Start by making a plan on how you will find the requested information.
2) Write this plan out so that the user can see your thought process.
3) Execute the plan (no need to wait for the confirmation from the user)
    by calling the tools and produce an answer to the user.

## Notes
- Do not make up information. Instead, find the way to answer
    the question by using tools at your disposal.
- If you, eventually, after using your tools, find out
    that you can not answer the question, say that you do not
    know the answer.
"""


def main():
    google_api_key = os.environ["GEMINI_API_KEY"]

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
            This function will always return a page of 10 sequential
            search results. Change the page_idx to get different pages.
        - Make sure that the name of the book is correctly spelled.
            by calling the list_books tool first.
            The tool will respond with an error message
            if the book is not found.

        ## Example
        Suppose that the user would like to know what color the hair
        of Harry Potter is:
        1) First, check whether Harry Potter books are in the library
        2) Use this tool to search for "Harry Potter" in any
        of these books and get books snippets
        3) Check the snippets for the hair color.
        4) Answer what the hair color is.
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

    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        google_project_id="gen-lang-client-0677234139",
    )

    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0.1,
        base_url="http://192.168.88.15:11434",
        tools=[library.list_books],
    )
    agent = create_agent(
        model=gemini_llm,
        system_prompt=SYSTEM_PROMPT,
        tools=[list_books, regex_search_book_paginated],
    )

    context = agent.invoke(
        {
            "messages": [
                # {"role": "user", "content": "List the books in the library."}
                {"role": "user", "content": "Can you describe captain Ahab?"}
            ]
        },
        print_mode="messages",
    )

    for msg in context["messages"]:
        if isinstance(msg, AIMessage):
            print(msg.text, end="")


if __name__ == "__main__":
    main()
