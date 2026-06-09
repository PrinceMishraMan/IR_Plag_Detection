import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

def build_train(base_dir):
    df = pd.read_csv(base_dir)
    X_real = df.drop("Label", axis=1).values
    y_real = df["Label"].values
    
    X_train, X_test, y_train, y_test = train_test_split(np.array(X_real), np.array(y_real), test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    from sklearn.model_selection import GridSearchCV
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, None],
        'min_samples_split': [2, 5, 10]
    }

    grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5)
    grid_search.fit(X_train_scaled, y_train)

    best_model = grid_search.best_estimator_
    # print(f"Best parameters found: {grid_search.best_params_}")

    predictions = best_model.predict(X_test_scaled)
    
    # print(classification_report(y_test, predictions))
    # print(confusion_matrix(y_test, predictions))
    print("True Positives:", np.sum((predictions == 1) & (y_test == 1)))
    print("True Negatives:", np.sum((predictions == 0) & (y_test == 0)))
    print("False Positives:", np.sum((predictions == 1) & (y_test == 0)))
    print("False Negatives:", np.sum((predictions == 0) & (y_test == 1)))
    print("Feature Importances:")
    for feature, importance in zip(df.columns[:-1], best_model.feature_importances_):
        print(f"{feature}: {importance:.4f}")
if __name__ == "__main__":
    dataset_directory = r"C:\Users\princ\Downloads\Programs\New_Plagiarism\real_features_1.csv"
    build_train(dataset_directory)