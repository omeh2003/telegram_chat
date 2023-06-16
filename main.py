import argparse
from datetime import datetime
from parsers.telegram_parser import parse_telegram_chat
from parsers.signal_parser import parse_signal_chat
from parsers.whatsapp_parser import parse_whatsapp_chat
from summarizers.gpt_summarizer import summarize_text as gpt_summarize_text
from summarizers.nltk_summarizer import summarize_text as nltk_summarize_text
from filters.date_filter import filter_messages_by_dates
from chunkers.word_count_chunker import chunk_text_by_word_count
from exporters.file_exporter import save_messages_to_file
from prompts.summary_prompt import generate_summary_prompt
from prompts.newsletter_prompt import generate_newsletter_prompt


def main(chat_export_file, summary_file, start_date, end_date, chat_type="Telegram", newsletter=False):
    # Чтение файла экспорта чата
    with open(chat_export_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Парсинг сообщений в зависимости от типа чата
    if chat_type == "Telegram":
        messages = parse_telegram_chat(content)
    elif chat_type == "Signal":
        messages = parse_signal_chat(content)
    elif chat_type == "WhatsApp":
        messages = parse_whatsapp_chat(content)
    else:
        print("Invalid chat type.")
        return

    # Преобразование дат начала и конца периода
    start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
    end_date = datetime.strptime(end_date, "%m/%d/%Y").date()

    # Фильтрация сообщений по датам
    filtered_messages = filter_messages_by_dates(messages, start_date, end_date)

    # Суммирование текста
    # filtered_messages=filtered_messages.split()
    # text = " ".join(filtered_messages)
    
    # Разделение текста на части с ограниченным количеством слов
    chunks = chunk_text_by_word_count(filtered_messages, max_word_count=1000)
    for message_from_sum in chunks:
        if newsletter:
            prompt = generate_newsletter_prompt(message_from_sum)
        else:
            prompt = generate_summary_prompt(message_from_sum)

        if chat_type != "Telegram":
            summary = gpt_summarize_text(prompt)
        else:
            summary = nltk_summarize_text(prompt)
        save_messages_to_file(summary, summary_file)

 

    # Сохранение резюме в файл
    save_messages_to_file(chunks, summary_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat_export_file", default=".\\ChatExport_2023-06-15\\result.json", help="Path to the chat export file")
    parser.add_argument("--summary_file",default="ChatExport_2023-06-15\\summary.txt" ,help="Path to the summary output file")
    parser.add_argument("--start_date", default="06/01/2023" , help="Start date for summarization (MM/DD/YYYY)")
    parser.add_argument("--end_date", default="06/16/2023" , help="End date for summarization (MM/DD/YYYY)")
    parser.add_argument("--chat_type", choices=["Telegram", "Signal", "WhatsApp"], default="Telegram",
                        help="Chat type (default: Telegram)")
    parser.add_argument("--newsletter",default=True ,action="store_true", help="Generate an introduction for a newsletter")

    args = parser.parse_args()

    main(
        args.chat_export_file,
        args.summary_file,
        args.start_date,
        args.end_date,
        args.chat_type,
        args.newsletter
    )
