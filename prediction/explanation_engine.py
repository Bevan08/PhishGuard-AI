def generate_explanations(
    ml_probability,
    analyzer_results,
    sender_analysis=None,
    header_analysis=None
):

    explanations = []

    # ==========================================
    # 1. AI MODEL EXPLANATION
    # ==========================================

    if ml_probability >= 80:
        explanations.append({
            "category": "AI Model",
            "severity": "HIGH",
            "message": (
                f"The AI model detected strong spam/phishing "
                f"characteristics with {ml_probability:.2f}% probability."
            )
        })

    elif ml_probability >= 50:
        explanations.append({
            "category": "AI Model",
            "severity": "MEDIUM",
            "message": (
                f"The AI model detected suspicious characteristics "
                f"with {ml_probability:.2f}% probability."
            )
        })

    else:
        explanations.append({
            "category": "AI Model",
            "severity": "LOW",
            "message": (
                f"The AI model found relatively few suspicious "
                f"characteristics ({ml_probability:.2f}% probability)."
            )
        })


    # ==========================================
    # 2. URL EXPLANATION
    # ==========================================

    for url in analyzer_results.get("url_details", []):

        if url.get("has_ip_address"):
            explanations.append({
                "category": "URL",
                "severity": "HIGH",
                "message": (
                    "The URL uses an IP address instead of a normal "
                    "domain name, which can be used to hide the "
                    "destination of a phishing website."
                )
            })

        if url.get("is_shortened"):
            explanations.append({
                "category": "URL",
                "severity": "MEDIUM",
                "message": (
                    "The email contains a shortened URL. "
                    "Shortened links can hide the actual destination."
                )
            })

        if url.get("has_at_symbol"):
            explanations.append({
                "category": "URL",
                "severity": "HIGH",
                "message": (
                    "The URL contains an @ symbol, a technique that "
                    "can be used to disguise the actual destination."
                )
            })

        if url.get("has_punycode"):
            explanations.append({
                "category": "URL",
                "severity": "HIGH",
                "message": (
                    "The URL contains punycode, which can sometimes "
                    "be used for lookalike or impersonation domains."
                )
            })

        if url.get("num_subdomains", 0) >= 3:
            explanations.append({
                "category": "URL",
                "severity": "MEDIUM",
                "message": (
                    "The URL contains multiple subdomains, which "
                    "can make a domain appear more trustworthy than it is."
                )
            })

        if url.get("url_length", 0) > 100:
            explanations.append({
                "category": "URL",
                "severity": "MEDIUM",
                "message": (
                    "The URL is unusually long, which can be a "
                    "characteristic of suspicious links."
                )
            })

        if url.get("suspicious_keywords"):
            keywords = ", ".join(
                url["suspicious_keywords"]
            )

            explanations.append({
                "category": "URL",
                "severity": "MEDIUM",
                "message": (
                    f"The URL contains suspicious keywords: {keywords}."
                )
            })

        if not url.get("uses_https"):
            explanations.append({
                "category": "URL",
                "severity": "MEDIUM",
                "message": (
                    "The URL does not use HTTPS, meaning the connection "
                    "does not provide standard HTTPS encryption."
                )
            })


    # ==========================================
    # 3. URGENCY EXPLANATION
    # ==========================================

    urgency_words = analyzer_results.get(
        "urgency_words", []
    )

    if urgency_words:

        explanations.append({
            "category": "Content",
            "severity": "MEDIUM",
            "message": (
                "The email uses urgency or pressure language "
                "that may attempt to make the recipient act quickly."
            )
        })


    # ==========================================
    # 4. CREDENTIAL EXPLANATION
    # ==========================================

    credential_words = analyzer_results.get(
        "credential_words", []
    )

    if credential_words:

        explanations.append({
            "category": "Credentials",
            "severity": "HIGH",
            "message": (
                "The email appears to request login credentials, "
                "passwords, verification codes, or account information."
            )
        })


    # ==========================================
    # 5. FINANCIAL EXPLANATION
    # ==========================================

    financial_words = analyzer_results.get(
        "financial_words", []
    )

    if financial_words:

        explanations.append({
            "category": "Financial",
            "severity": "HIGH",
            "message": (
                "The email contains banking, payment, transaction, "
                "refund, or financial-related language."
            )
        })


    # ==========================================
    # 6. SENDER EXPLANATION
    # ==========================================

    if sender_analysis:

        sender_reasons = sender_analysis.get(
            "sender_reasons", []
        )

        for reason in sender_reasons:

            explanations.append({
                "category": "Sender",
                "severity": "HIGH",
                "message": reason
            })


    # ==========================================
    # 7. HEADER EXPLANATION
    # ==========================================

    if header_analysis:

        header_warnings = header_analysis.get(
            "warnings", []
        )

        for warning in header_warnings:

            explanations.append({
                "category": "Email Header",
                "severity": "HIGH",
                "message": warning
            })


    # ==========================================
    # 8. REMOVE DUPLICATES
    # ==========================================

    unique_explanations = []

    seen = set()

    for explanation in explanations:

        key = (
            explanation["category"],
            explanation["message"]
        )

        if key not in seen:

            seen.add(key)

            unique_explanations.append(
                explanation
            )


    return unique_explanations