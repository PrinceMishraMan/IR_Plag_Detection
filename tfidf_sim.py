import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_java_code(code):
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    code = re.sub(r'//.*', '', code)
    return re.sub(r'\"[^\"]*\"', '', code)

def java_tfidf_similarity(code1, code2):
    try:
        tokens1 = re.findall(r'\b\w+\b', clean_java_code(code1))
        tokens2 = re.findall(r'\b\w+\b', clean_java_code(code2))
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([' '.join(tokens1), ' '.join(tokens2)])
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        return 0.0