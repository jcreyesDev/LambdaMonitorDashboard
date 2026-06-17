import re
from collections import Counter

def lambda_handler(event, context):
    text = event.get('text', '')

    characters = len(text)
    words = len(text.split())
    sentences = text.count('.') + text.count('?') + text.count('!')
    paragraphs = len([p for p in text.split('\n') if p.strip()])

    clean_text = re.sub(r'[.!?,;:]', '', text.lower())
    word_list = clean_text.split()
    word_count = Counter(word_list).most_common(1)
    most_frecuent_words = word_count[0][0] if word_count and word_count[0][1] > 1 else None

    char_list = [c for c in text.lower() if c.isalpha()]
    char_count = Counter(char_list).most_common(1)
    most_frecuent_characters = char_count[0][0] if char_count and char_count[0][1] > 1 else None

    return {
        'statusCode': 200,
        'body': {
            'characters': characters,
            'words': words,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'most_frequent_words': most_frecuent_words,
            'most_frequent_characters': most_frecuent_characters
        }
    }