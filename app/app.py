from flask import Flask, render_template, request

import joblib
import os

from prediction.phishing_analyzer import analyze_email
from prediction.risk_engine import calculate_risk_score
from prediction.sender_analyzer import analyze_senders
from prediction.header_analyzer import analyze_headers
from prediction.explanation_engine import generate_explanations


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# LOAD AI MODEL
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)


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
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        email_text = request.form.get("email", "").strip()

        # Handle uploaded email file
        uploaded_file = request.files.get("email_file")

        if uploaded_file and uploaded_file.filename:

            filename = uploaded_file.filename.lower()

            if filename.endswith(".txt"):

                email_text = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            elif filename.endswith(".eml"):

                email_text = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            else:

                return render_template(
                    "index.html",
                    result={
                        "error": "Please upload a .txt or .eml file."
                    }
                )

        if not email_text:

            return render_template(
                "index.html",
                result={
                    "error": "Please paste an email or upload a file."
                }
            )

        # ------------------------------
        # AI MODEL
        # ------------------------------

        email_vector = vectorizer.transform(
            [email_text]
        )

        prediction = model.predict(
            email_vector
        )

        probability = model.predict_proba(
            email_vector
        )

        # Find the correct positive class (spam)
        classes = list(model.classes_)

        if "spam" in classes:
            positive_index = classes.index("spam")
        elif 1 in classes:
            positive_index = classes.index(1)
        else:
            positive_index = 1

        ml_probability = probability[0][positive_index] * 100


        # ------------------------------
        # SECURITY ANALYSIS
        # ------------------------------

        analysis = analyze_email(
            email_text
        )

        header_analysis = analyze_headers(
            email_text
        )

        sender_analysis = analyze_senders(
            email_text
        )

        # ------------------------------
        # RISK SCORE
        # ------------------------------

        risk_score, risk_level, reasons = calculate_risk_score(
            ml_probability,
            analysis,
            sender_analysis,
            header_analysis
        )

        explanations = generate_explanations(
            ml_probability,
            analysis,
            sender_analysis,
            header_analysis
        )

        result = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "ml_probability": round(
                ml_probability,
                2
            ),
            "urls": analysis["urls"],
            "url_reasons": analysis["url_reasons"],
            "urgency_words": analysis["urgency_words"],
            "credential_words": analysis["credential_words"],
            "financial_words": analysis["financial_words"],
            "header_analysis": header_analysis,
            "sender_analysis": sender_analysis,
            "explanations": explanations,
            "reasons": reasons
        }


    return render_template(
        "index.html",
        result=result
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )