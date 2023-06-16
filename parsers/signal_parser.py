import re


def parse_signal_chat(content):
    messages = re.findall(r'"text": "(.*?)"', content)
    return messages
