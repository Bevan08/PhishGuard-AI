import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv("dataset/cleaned_emails.csv")

print("Dataset loaded successfully!")
print("Total emails:", len(data))


# ==========================================
# 2. INPUT AND OUTPUT
# ==========================================

X = data["text"]
y = data["label"]


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. TF-IDF
# ==========================================

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english",
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)


print("\nTF-IDF conversion completed!")
print(
    "Number of features:",
    len(vectorizer.get_feature_names_out())
)


# ==========================================
# 5. CREATE MODELS
# ==========================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=1000
        ),

    "Naive Bayes":
        MultinomialNB(),

    "Linear SVM":
        LinearSVC(),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        )
}


# ==========================================
# 6. TRAIN AND EVALUATE
# ==========================================

results = []


for name, model in models.items():

    print("\n" + "=" * 60)
    print("Training:", name)
    print("=" * 60)

    model.fit(
        X_train_tfidf,
        y_train
    )

    y_pred = model.predict(
        X_test_tfidf
    )


    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )


    results.append({

        "Model": name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Score": f1
    })


    print(
        f"Accuracy : {accuracy * 100:.2f}%"
    )

    print(
        f"Precision: {precision * 100:.2f}%"
    )

    print(
        f"Recall   : {recall * 100:.2f}%"
    )

    print(
        f"F1 Score : {f1 * 100:.2f}%"
    )


# ==========================================
# 7. COMPARISON TABLE
# ==========================================

results_df = pd.DataFrame(results)


print("\n\n")
print("=" * 75)
print("MODEL COMPARISON")
print("=" * 75)

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1 Score": "{:.4f}".format
        }
    )
)


# ==========================================
# 8. FIND BEST MODEL
# ==========================================

best_model = results_df.loc[
    results_df["F1 Score"].idxmax()
]


print("\n")
print("=" * 75)
print("BEST MODEL")
print("=" * 75)

print(
    "Model:",
    best_model["Model"]
)

print(
    f"F1 Score: {best_model['F1 Score'] * 100:.2f}%"
)