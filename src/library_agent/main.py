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
        "Lists all available books"
        return library.list_books()


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
        tools=[list_books],
    )

    context = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "what books do you have?"}
            ]
        },
    )

    for msg in context["messages"]:
        if isinstance(msg, AIMessage):
            print(msg.content)


if __name__ == "__main__":
    main()
