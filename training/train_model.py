import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv("dataset/cleaned_emails.csv")

print("Dataset loaded successfully!")
print("Total emails:", len(data))


# ==========================================
# 2. SPLIT INPUT AND OUTPUT
# ==========================================

X = data["text"]
y = data["label"]


print("\nClass distribution:")
print(y.value_counts())


# ==========================================
# 3. SPLIT TRAINING AND TEST DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining emails:", len(X_train))
print("Testing emails:", len(X_test))


# ==========================================
# 4. TF-IDF FEATURE EXTRACTION
# ==========================================

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words="english",
    ngram_range=(1, 2)
)


X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)


print("\nTF-IDF conversion completed!")
print("Number of features:", len(vectorizer.get_feature_names_out()))


# ==========================================
# 5. CREATE LOGISTIC REGRESSION MODEL
# ==========================================

model = LogisticRegression(
    max_iter=1000
)


# ==========================================
# 6. TRAIN MODEL
# ==========================================

print("\nTraining Logistic Regression model...")

model.fit(
    X_train_tfidf,
    y_train
)

print("Model training completed!")


# ==========================================
# 7. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(
    X_test_tfidf
)


# Probability for ROC-AUC
y_probability = model.predict_proba(
    X_test_tfidf
)


# ==========================================
# 8. EVALUATE MODEL
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n")
print("=" * 50)
print("MODEL EVALUATION")
print("=" * 50)


print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

print("\nClassification Report:")
print("-" * 50)

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

print("\nConfusion Matrix:")
print("-" * 50)

matrix = confusion_matrix(
    y_test,
    y_pred
)

print(matrix)


# ==========================================
# ROC-AUC
# ==========================================

try:

    # For binary classification, use probability
    # of the positive class.

    positive_class = model.classes_[1]

    positive_index = list(
        model.classes_
    ).index(
        positive_class
    )

    y_probability_positive = y_probability[
        :, positive_index
    ]

    auc_score = roc_auc_score(
        y_test,
        y_probability_positive
    )

    print(
        f"\nROC-AUC Score: {auc_score:.4f}"
    )

except Exception as error:

    print(
        "\nROC-AUC could not be calculated:"
    )

    print(error)


# ==========================================
# MODEL INFORMATION
# ==========================================

print("\nModel classes:")

print(model.classes_)


# ==========================================
# SAVE TRAINED MODEL
# ==========================================

joblib.dump(
    model,
    "model/phishing_model.pkl"
)

joblib.dump(
    vectorizer,
    "model/tfidf_vectorizer.pkl"
)


print("\n" + "=" * 50)
print("MODEL SAVED")
print("=" * 50)

print(
    "\nModel:"
    "\nmodel/phishing_model.pkl"
)

print(
    "\nVectorizer:"
    "\nmodel/tfidf_vectorizer.pkl"
)