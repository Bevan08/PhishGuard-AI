import os
import joblib


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(
    os.path.join(
        BASE_DIR,
        "model",
        "phishing_model.pkl"
    )
)

vectorizer = joblib.load(
    os.path.join(
        BASE_DIR,
        "model",
        "tfidf_vectorizer.pkl"
    )
)


# ==========================================
# EMAIL TO TEST
# ==========================================

email = """
URGENT! Your bank account will be suspended.
Verify your identity immediately by clicking this link.
Please provide your username, password and OTP.
"""


# ==========================================
# TRANSFORM EMAIL
# ==========================================

email_vector = vectorizer.transform([email])


# ==========================================
# PREDICTION
# ==========================================

prediction = model.predict(email_vector)

probabilities = model.predict_proba(email_vector)[0]


# ==========================================
# FIND SPAM PROBABILITY
# ==========================================

classes = list(model.classes_)

if "spam" in classes:
    positive_index = classes.index("spam")
elif 1 in classes:
    positive_index = classes.index(1)
else:
    positive_index = 1


spam_probability = probabilities[positive_index] * 100
legitimate_probability = 100 - spam_probability


# ==========================================
# DISPLAY RESULT
# ==========================================

print("=" * 60)
print("AI PHISHING EMAIL DETECTOR")
print("=" * 60)

print()

if spam_probability >= 50:

    print("🚨 SPAM / PHISHING EMAIL")

else:

    print("✅ LEGITIMATE EMAIL")


print()

print(
    f"Spam probability: "
    f"{spam_probability:.2f}%"
)

print(
    f"Legitimate probability: "
    f"{legitimate_probability:.2f}%"
)

print()

print("Model prediction:", prediction[0])

print("=" * 60)