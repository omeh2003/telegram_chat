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
