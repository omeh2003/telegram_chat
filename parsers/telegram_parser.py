import json


def parse_telegram_chat(content):
    data = json.loads(content)
    messages = data.get("messages", [])
    parsed_messages = []

    for message in messages:
        if "text" in message:
            text = message["text"]
            parsed_messages.append(text)

    return parsed_messages
