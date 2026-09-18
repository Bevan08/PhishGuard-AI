import re
from urllib.parse import urlparse


# ==========================================
# EXTRACT EMAIL ADDRESSES
# ==========================================

def extract_email_addresses(email_text):

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    return re.findall(
        pattern,
        email_text
    )


# ==========================================
# ANALYZE EMAIL ADDRESS
# ==========================================

def analyze_sender(email_address):

    reasons = []

    email_address = email_address.lower().strip()

    # Basic validation
    if "@" not in email_address:

        reasons.append(
            "Invalid email address format"
        )

        return reasons

    username, domain = email_address.split(
        "@",
        1
    )

    # IP address used as domain
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    if re.match(ip_pattern, domain):

        reasons.append(
            "Sender uses an IP address instead of a domain"
        )

    # Suspicious words in domain
    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "support",
        "password",
        "security"
    ]

    for word in suspicious_words:

        if word in domain:

            reasons.append(
                f"Sender domain contains suspicious word: {word}"
            )

            break

    # Excessive subdomains
    if domain.count(".") >= 3:

        reasons.append(
            "Sender domain contains many subdomains"
        )

    # Very long domain
    if len(domain) > 40:

        reasons.append(
            "Sender domain is unusually long"
        )

    return reasons


# ==========================================
# ANALYZE EMAIL SENDER
# ==========================================

def analyze_senders(email_text):

    senders = extract_email_addresses(
        email_text
    )

    results = {
        "senders": senders,
        "sender_reasons": []
    }

    for sender in senders:

        reasons = analyze_sender(
            sender
        )

        results["sender_reasons"].extend(
            reasons
        )

    return results