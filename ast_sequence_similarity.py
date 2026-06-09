import javalang
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def java_ast_sequence_similarity(code1, code2):
    def get_node_sequence(code):
        try:
            tree = javalang.parse.parse(code)
            return " ".join([type(node).__name__ for path, node in tree])
        except:
            return ""
            
    seq1, seq2 = get_node_sequence(code1), get_node_sequence(code2)
    if not seq1 or not seq2: return 0.0
    
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([seq1, seq2])
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        return 0.0