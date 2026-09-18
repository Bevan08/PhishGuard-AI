import re

from prediction.url_analyzer import analyze_url


# ==========================================
# SUSPICIOUS KEYWORDS
# ==========================================

URGENCY_WORDS = [
    "urgent",
    "immediately",
    "right now",
    "act now",
    "within 24 hours",
    "as soon as possible",
    "final warning",
    "last warning",
    "expires",
    "suspended",
    "blocked",
    "limited"
]


CREDENTIAL_WORDS = [
    "password",
    "username",
    "login",
    "log in",
    "verify your identity",
    "verification",
    "credentials",
    "security code",
    "otp",
    "one time password"
]


FINANCIAL_WORDS = [
    "bank",
    "bank account",
    "credit card",
    "debit card",
    "payment",
    "transaction",
    "refund",
    "money",
    "account number",
    "upi"
]


# ==========================================
# EXTRACT URLs
# ==========================================

def extract_urls(email_text):

    url_pattern = r"https?://[^\s]+|www\.[^\s]+"

    urls = re.findall(
        url_pattern,
        email_text
    )

    return urls


# ==========================================
# FIND KEYWORDS
# ==========================================

def find_keywords(email_text, keywords):

    found = []

    text = email_text.lower()

    for keyword in keywords:

        if keyword in text:
            found.append(keyword)

    return found


# ==========================================
# ANALYZE EMAIL
# ==========================================

def analyze_email(email_text):

    results = {

        "urls": [],

        "url_reasons": [],

        "url_details": [],

        "urgency_words": [],

        "credential_words": [],

        "financial_words": []
    }


    # ======================================
    # Extract URLs
    # ======================================

    urls = extract_urls(email_text)

    results["urls"] = urls


    # ======================================
    # Advanced URL Analysis
    # ======================================

    for url in urls:

        url_analysis = analyze_url(url)

        # Store complete URL feature information
        results["url_details"].append(
            url_analysis
        )

        # Store warnings/reasons
        results["url_reasons"].extend(
            url_analysis["warnings"]
        )


    # ======================================
    # Find suspicious words
    # ======================================

    results["urgency_words"] = find_keywords(
        email_text,
        URGENCY_WORDS
    )


    results["credential_words"] = find_keywords(
        email_text,
        CREDENTIAL_WORDS
    )


    results["financial_words"] = find_keywords(
        email_text,
        FINANCIAL_WORDS
    )


    return results