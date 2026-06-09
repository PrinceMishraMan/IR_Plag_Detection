import hashlib
import re
from clean_java import clean_java_code

def winnowing_similarity(code1, code2, k=15, w=4):
    def get_fingerprints(text):
        text = re.sub(r'\s+', '', text)
        if len(text) < k: return set()
        hashes = [int(hashlib.md5(text[i:i+k].encode('utf-8')).hexdigest(), 16) for i in range(len(text) - k + 1)]
        fingerprints = set()
        for i in range(len(hashes) - w + 1):
            fingerprints.add(min(hashes[i:i+w]))
        return fingerprints

    fp1 = get_fingerprints(clean_java_code(code1))
    fp2 = get_fingerprints(clean_java_code(code2))
    
    if not fp1 or not fp2: return 0.0
    intersection = len(fp1.intersection(fp2))
    union = len(fp1.union(fp2))
    return intersection / union if union > 0 else 0.0