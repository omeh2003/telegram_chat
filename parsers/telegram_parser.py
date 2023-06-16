import json


def parse_telegram_chat(content):
    data = json.loads(content)
    messages = data.get("messages", [])
    parsed_messages = []

    for message in messages:
        text={}
        if message['type']=="message":
            if message['text_entities']:
                if message['text_entities'][0]['type'] =="plain":
                    if message['text']:
                        if isinstance(message['text'],list):
                            text['text']= message['text'][0]
                            text['date'] = message['date']
                        if isinstance(message['text'],str):
                            text['text'] = message["text"]
                            text['date'] = message['date']
                        parsed_messages.append(text)

    return parsed_messages
