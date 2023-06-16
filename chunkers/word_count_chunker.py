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
