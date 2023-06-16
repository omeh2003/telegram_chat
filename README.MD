```
telegram_chat/
    ├── main.py
    ├── utils.py
    ├── parsers/
    │   ├── telegram_parser.py
    │   ├── signal_parser.py
    │   └── whatsapp_parser.py
    ├── summarizers/
    │   ├── gpt_summarizer.py
    │   └── nltk_summarizer.py
    ├── models/
    │   └── gpt_model.py
    ├── filters/
    │   └── date_filter.py
    ├── chunkers/
    │   └── word_count_chunker.py
    ├── exporters/
    │   └── file_exporter.py
    └── prompts/
        ├── newsletter_prompt.py
        └── summary_prompt.py
```

- `main.py`: Основной файл, который содержит логику программы и вызывает соответствующие функции.
- `utils.py`: Вспомогательные функции и константы, которые используются в разных частях программы.
- `parsers/`: Пакет, содержащий модули для парсинга сообщений из разных источников (Telegram, Signal, WhatsApp).
- `summarizers/`: Пакет, содержащий модули для суммирования текста с использованием разных алгоритмов и моделей (GPT,
  NLTK).
- `models/`: Пакет, содержащий модули для работы с моделями (GPT, NLTK).
- `filters/`: Пакет, содержащий модули для фильтрации сообщений по датам.
- `chunkers/`: Пакет, содержащий модули для разделения текста на части с ограниченным количеством слов.
- `exporters/`: Пакет, содержащий модули для экспорта данных (сохранение сообщений в файл).
- `prompts/`: Пакет, содержащий модули для генерации промптов для моделей GPT.

Такая структура проекта позволяет легко добавлять новые функции и модули, а также обеспечивает четкое разделение
ответственности между различными частями программы.

Часть 3: Установка зависимостей

Для выполнения данной задачи вам понадобятся следующие зависимости:

- Python 3.10: Убедитесь, что у вас установлена версия Python 3.10 или выше. Вы можете проверить версию Python, выполнив
  команду `python --version` в командной строке.
- Библиотеки Python: Вам понадобятся следующие библиотеки Python, которые можно установить с помощью менеджера
  пакетов `pip`:

    - `openai`: Для взаимодействия с моделью GPT от OpenAI. Установите его с помощью команды `pip install openai`.
    - `nltk`: Для обработки естественного языка и суммирования текста с использованием алгоритмов NLTK. Установите его с
      помощью команды `pip install nltk`.

- Дополнительные программы: Вам также понадобятся следующие программы:

    - OpenAI API Key: Для использования модели GPT от OpenAI вам понадобится ключ API. Вы можете получить его,
      зарегистрировавшись на сайте OpenAI.
    - NLTK Data: Для использования алгоритмов суммирования текста от NLTK вам понадобятся дополнительные данные. Вы
      можете загрузить их, выполнив следующую команду в Python:

```python
import nltk

nltk.download('punkt')
```

Установка зависимостей завершена. Теперь

**Часть 4: Реализация кода**

В этой части я представлю реализацию кода для каждой из функций, описанных в плане реализации.

**Модуль `telegram_parser.py`:**

```python
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
```

**Модуль `signal_parser.py`:**

```python
import re


def parse_signal_chat(content):
    messages = re.findall(r'"text": "(.*?)"', content)
    return messages
```

**Модуль `whatsapp_parser.py`:**

```python
def parse_whatsapp_chat(content):
    messages = content.split("\n")
    return messages
```

**Модуль `gpt_summarizer.py`:**

```python
import openai


def summarize_text(text):
    model = "gpt-4"
    messages = [{"role": "user", "content": text}]
    completion = openai.ChatCompletion.create(model=model, messages=messages)
    response = completion.choices[0].message.content
    return response
```

**Модуль `nltk_summarizer.py`:**

```python
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def summarize_text(text):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    word_frequencies = {}
    for sentence in sentences:
        for word in sentence.split():
            word = stemmer.stem(word.lower())
            if word not in stop_words:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_scores = {}
    for sentence in sentences:
        for word in sentence.split():
            word = stemmer.stem(word.lower())
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = " ".join(summary_sentences[:3])  # Get the top 3 sentences

    return summary
```

**Модуль `date_filter.py`:**

```python
from datetime import datetime


def filter_messages_by_dates(messages, start_date, end_date):
    filtered_messages = []
    for message in messages:
        date_str = message.get("date")
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            if start_date <= date <= end_date:
                filtered_messages.append(message)

    return filtered_messages
```

**Модуль `word_count_chunker.py`:**

```python
def chunk_text_by_word_count(text, max_word_count):
    chunks = []
    current_chunk = ""
    current_word_count = 0

    words = text.split()
    for word in words:
        current_chunk += word + " "
        current_word_count += 1

        if current_word_count >= max_word_count:
            chunks.append(current_chunk.strip())
            current_chunk = ""
            current_word_count = 0

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
```

**Модуль `file_exporter.py`:**

```python
def save_messages_to_file(messages, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for message in messages:
            file.write(message + "\n")
```

**Модуль `summary_prompt.py`:**

```python
SUMMARY_PROMPT = """Пожалуйста, суммируйте следующий чат Telegram на основе обсуждаемых тем. Для каждой темы укажите ее заголовок и краткое содержание в виде маркированных пунктов. В пунктах должна содержаться подробная информация. Если в теме содержатся рекомендации относительно конкретных компаний или услуг, пожалуйста, включите их в резюме. Пожалуйста, включите также ссылки, которые были разделены."""


def generate_summary_prompt(chat):
    prompt = f"{SUMMARY_PROMPT}\n\n{chat}"
    return prompt
```

**Модуль `newsletter_prompt.py`:**

```python
NEWSLETTER_PROMPT = """Пожалуйста, предоставьте один абзац для открытия информационного бюллетеня, охватывающего следующие темы:"""


def generate_newsletter_prompt(chat):
    prompt = f"{NEWSLETTER_PROMPT}\n\n{chat}"
    return prompt
```

**Основной модуль `main.py`:**

```python
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
    text = " ".join(filtered_messages)
    if newsletter:
        prompt = generate_newsletter_prompt(text)
    else:
        prompt = generate_summary_prompt(text)

    if chat_type == "Telegram":
        summary = gpt_summarize_text(prompt)
    else:
        summary = nltk_summarize_text(prompt)

    # Разделение текста на части с ограниченным количеством слов
    chunks = chunk_text_by_word_count(summary, max_word_count=2500)

    # Сохранение резюме в файл
    save_messages_to_file(chunks, summary_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat_export_file", help="Path to the chat export file")
    parser.add_argument("summary_file", help="Path to the summary output file")
    parser.add_argument("start_date", help="Start date for summarization (MM/DD/YYYY)")
    parser.add_argument("end_date", help="End date for summarization (MM/DD/YYYY)")
    parser.add_argument("--chat_type", choices=["Telegram", "Signal", "WhatsApp"], default="Telegram",
                        help="Chat type (default: Telegram)")
    parser.add_argument("--newsletter", action="store_true", help="Generate an introduction for a newsletter")

    args = parser.parse_args()

    main(
        args.chat_export_file,
        args.summary_file,
        args.start_date,
        args.end_date,
        args.chat_type,
        args.newsletter
    )
```