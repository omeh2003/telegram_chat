NEWSLETTER_PROMPT = """Пожалуйста, предоставьте один абзац для открытия информационного бюллетеня, охватывающего 
следующие темы:"""


def generate_newsletter_prompt(chat):
    prompt = f"{NEWSLETTER_PROMPT}\n\n{chat}"
    return prompt
