from library_agent.agent import gemini_agent
from langchain.messages import AIMessage


def main():
    context = gemini_agent.invoke(
        {
            "messages": [
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
