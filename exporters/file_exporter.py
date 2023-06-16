def save_messages_to_file(messages, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for message in messages:
            file.write(message + "\n")
