import re

def clean_java_code(code):
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    code = re.sub(r'//.*', '', code)
    return re.sub(r'\"[^\"]*\"', '', code)