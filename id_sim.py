import javalang

def java_identifier_similarity(code1, code2):
    def extract_ids(tree):
        ids = []
        if tree:
            for path, node in tree:
                if isinstance(node, (javalang.tree.ClassDeclaration, javalang.tree.MethodDeclaration, javalang.tree.VariableDeclarator)):
                    ids.append(node.name)
        return ids
    try:
        ids1 = set(extract_ids(javalang.parse.parse(code1)))
        ids2 = set(extract_ids(javalang.parse.parse(code2)))
        if not ids1 or not ids2: return 0.0
        union = len(ids1.union(ids2))
        return len(ids1.intersection(ids2)) / union if union > 0 else 0.0
    except:
        return 0.0