import javalang

def get_cyclomatic_complexity(code):
    try:
        tree = javalang.parse.parse(code)
        complexity = 1
        for path, node in tree:
            if isinstance(node, (javalang.tree.IfStatement, 
                                 javalang.tree.WhileStatement, 
                                 javalang.tree.ForStatement, 
                                 javalang.tree.DoStatement,
                                 javalang.tree.SwitchStatementCase, 
                                 javalang.tree.CatchClause)):
                complexity += 1
        return complexity
    except:
        return 0

def cyclomatic_similarity(code1, code2):
    comp1 = get_cyclomatic_complexity(code1)
    comp2 = get_cyclomatic_complexity(code2)
    
    if comp1 == 0 and comp2 == 0: 
        return 0.0
    return min(comp1, comp2) / max(comp1, comp2)