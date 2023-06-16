from datetime import datetime


def filter_messages_by_dates(messages, start_date, end_date):
    filtered_messages = ""
    for message in messages:
        date_str = message.get("date")
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
            if start_date <= date <= end_date:
                filtered_messages+=message['text']

    return filtered_messages
