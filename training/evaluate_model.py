import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve
)


# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv("dataset/cleaned_emails.csv")

X = data["text"]
y = data["label"]


# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

model = joblib.load(
    "model/phishing_model.pkl"
)

vectorizer = joblib.load(
    "model/tfidf_vectorizer.pkl"
)

print("Model and vectorizer loaded successfully!")


# ==========================================
# 3. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 4. TF-IDF TRANSFORMATION
# ==========================================

X_test_tfidf = vectorizer.transform(X_test)


# ==========================================
# 5. PREDICTIONS
# ==========================================

y_pred = model.predict(
    X_test_tfidf
)

y_probability = model.predict_proba(
    X_test_tfidf
)

positive_class = model.classes_[1]

positive_index = list(
    model.classes_
).index(
    positive_class
)

y_probability_positive = y_probability[
    :, positive_index
]


# ==========================================
# 6. ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


# ==========================================
# 7. CLASSIFICATION REPORT
# ==========================================

print("\nClassification Report:")
print("-" * 60)

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ==========================================
# 8. CONFUSION MATRIX
# ==========================================

matrix = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print("-" * 60)

print(matrix)


# ==========================================
# 9. ROC-AUC
# ==========================================

auc_score = roc_auc_score(
    y_test,
    y_probability_positive
)

print(
    f"\nROC-AUC Score: {auc_score:.4f}"
)


# ==========================================
# 10. SAVE CONFUSION MATRIX
# ==========================================

plt.figure()

plt.imshow(matrix)

plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")

plt.xticks(
    [0, 1],
    ["Legitimate", "Spam/Phishing"]
)

plt.yticks(
    [0, 1],
    ["Legitimate", "Spam/Phishing"]
)

for i in range(2):
    for j in range(2):
        plt.text(
            j,
            i,
            matrix[i, j],
            ha="center",
            va="center"
        )

plt.colorbar()

plt.tight_layout()

plt.savefig(
    "training/confusion_matrix.png",
    dpi=300
)

plt.close()


# ==========================================
# 11. ROC CURVE
# ==========================================

fpr, tpr, thresholds = roc_curve(
    y_test,
    y_probability_positive
)

plt.figure()

plt.plot(
    fpr,
    tpr,
    label=f"Logistic Regression (AUC = {auc_score:.4f})"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()

plt.tight_layout()

plt.savefig(
    "training/roc_curve.png",
    dpi=300
)

plt.close()


# ==========================================
# 12. FINAL OUTPUT
# ==========================================

print("\n" + "=" * 60)
print("EVALUATION COMPLETED")
print("=" * 60)

print("\nSaved files:")

print(
    "training/confusion_matrix.png"
)

print(
    "training/roc_curve.png"
)