import Levenshtein
from clean_java import clean_java_code

def java_levenshtein_similarity(code1, code2):
    return Levenshtein.ratio(clean_java_code(code1), clean_java_code(code2))