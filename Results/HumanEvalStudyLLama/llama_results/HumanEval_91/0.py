import re

def is_bored(S):
    sentences = re.split('[.!?]', S)
    return sum(1 for sentence in sentences if sentence.strip() and sentence.strip().lower().startswith('i'))