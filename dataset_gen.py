import numpy as np
import pandas as pd
import glob
import os
import Levenshtein
from clean_java import clean_java_code
from id_sim import java_identifier_similarity
from tfidf_sim import java_tfidf_similarity
from cyclomatic_similarity import cyclomatic_similarity
from levenshtein_similarity import java_levenshtein_similarity
from ast_sequence_similarity import java_ast_sequence_similarity
from win_sim import winnowing_similarity

def extract_java_features(code1, code2):
    
    # 1. ID Sim, 2. TF-IDF, 3. Word Len, 4. Char Len, 5. Levenshtein, 6. AST, 7. Winnowing, 8. Cyclomatic
    
    try:
        features = [
            java_identifier_similarity(code1, code2),
            java_tfidf_similarity(code1, code2),
            min(len(code1.split()), len(code2.split())) / max(len(code1.split()), len(code2.split())) if max(len(code1.split()), len(code2.split())) > 0 else 0.0,
            min(len(clean_java_code(code1)), len(clean_java_code(code2))) / max(len(clean_java_code(code1)), len(clean_java_code(code2))) if max(len(clean_java_code(code1)), len(clean_java_code(code2))) > 0 else 0.0,
            java_levenshtein_similarity(code1, code2),
            java_ast_sequence_similarity(code1, code2),
            winnowing_similarity(code1, code2),
            cyclomatic_similarity(code1, code2)
        ]
    except Exception as e:
        clean1, clean2 = clean_java_code(code1), clean_java_code(code2)
        features = [
            0.0, # ID
            java_tfidf_similarity(code1, code2),
            min(len(code1.split()), len(code2.split())) / max(len(code1.split()), len(code2.split())) if max(len(code1.split()), len(code2.split())) > 0 else 0.0,
            min(len(clean1), len(clean2)) / max(len(clean1), len(clean2)) if max(len(clean1), len(clean2)) > 0 else 0.0,
            Levenshtein.ratio(clean1, clean2),
            0.0, # AST
            winnowing_similarity(code1, code2),
            0.0  # Cyclomatic
        ]
        
    return np.array(features).reshape(1, -1)

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def build_dataset(base_dir):
    X_real = []
    y_real = []
    
    for problem in os.listdir(base_dir):
        problem_path = os.path.join(base_dir, problem)
        if not os.path.isdir(problem_path): continue

        original_dir = os.path.join(problem_path, "original")
        plag_dir = os.path.join(problem_path, "plagiarized")
        nonplag_dir = os.path.join(problem_path, "non-plagiarized")

        if not all(os.path.exists(d) for d in [original_dir, plag_dir, nonplag_dir]):
            continue

        original_files = [os.path.join(original_dir, f) for f in os.listdir(original_dir) if f.endswith(".java")]
        plag_files = glob.glob(os.path.join(plag_dir, '**', '*.java'), recursive=True)
        nonplag_files = glob.glob(os.path.join(nonplag_dir, '**', '*.java'), recursive=True)

        for orig_file in original_files:
            orig_code = read_file(orig_file)

            # Plagiarized = Label 1
            for plag_file in plag_files:
                plag_code = read_file(plag_file)
                features = extract_java_features(orig_code, plag_code)[0]
                X_real.append(features)
                y_real.append(1)

            # Non-Plagiarized = Label 0
            for nonplag_file in nonplag_files:
                nonplag_code = read_file(nonplag_file)
                features = extract_java_features(orig_code, nonplag_code)[0]
                X_real.append(features)
                y_real.append(0)

    df = pd.DataFrame(X_real, columns=[
        "ID_Sim", "TFIDF_Sim", "Word_Len_Ratio", "Char_Len_Ratio", 
        "Levenshtein_Sim", "AST_Sim", "Winnowing_Sim", "Cyclomatic_Sim"
    ])
    df["Label"] = y_real
    df.to_csv("real_features_1.csv", index=False)
    print("Successfully saved to real_features_1.csv!")
if __name__ == "__main__":
    dataset_directory = r"C:\Users\princ\Downloads\Programs\New_Plagiarism\IR-Plag-Dataset"  # Change this to your dataset path
    build_dataset(dataset_directory)