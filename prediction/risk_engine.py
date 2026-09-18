def calculate_risk_score(
    ml_probability,
    analyzer_results,
    sender_analysis=None,
    header_analysis=None
):

    score = 0
    reasons = []

    # ==========================================
    # AI MODEL
    # ==========================================

    ml_score = round(ml_probability * 0.50)

    score += ml_score

    if ml_probability >= 50:
        reasons.append(
            "AI model detected strong spam/phishing characteristics"
        )


    # ==========================================
    # URL ANALYSIS
    # ==========================================

    url_score = 0

    for url in analyzer_results.get("url_details", []):

        if url.get("has_ip_address"):
            url_score += 15

        if url.get("is_shortened"):
            url_score += 8

        if url.get("has_at_symbol"):
            url_score += 10

        if url.get("has_punycode"):
            url_score += 12

        if url.get("num_subdomains", 0) >= 3:
            url_score += 8

        if url.get("url_length", 0) > 100:
            url_score += 5

        if url.get("domain_length", 0) > 50:
            url_score += 5

        if url.get("suspicious_keywords"):
            url_score += min(
                len(url["suspicious_keywords"]) * 3,
                12
            )

        if not url.get("uses_https"):
            url_score += 3


    url_score = min(url_score, 35)

    score += url_score

    if url_score > 0:
        reasons.append(
            "Suspicious URL characteristics detected"
        )


    # ==========================================
    # CONTENT ANALYSIS
    # ==========================================

    if analyzer_results.get("urgency_words"):

        score += 10

        reasons.append(
            "Urgency or threat language detected"
        )


    if analyzer_results.get("credential_words"):

        score += 15

        reasons.append(
            "Credential or account verification request detected"
        )


    if analyzer_results.get("financial_words"):

        score += 10

        reasons.append(
            "Financial or banking-related language detected"
        )


    # ==========================================
    # SENDER ANALYSIS
    # ==========================================

    sender_reasons = []

    if sender_analysis:

        sender_reasons = sender_analysis.get(
            "sender_reasons",
            []
        )

    if sender_reasons:

        score += min(
            len(sender_reasons) * 8,
            20
        )

        reasons.extend(sender_reasons)


    # ==========================================
    # HEADER ANALYSIS
    # ==========================================

    header_warnings = []

    if header_analysis:

        header_warnings = header_analysis.get(
            "warnings",
            []
        )

    if header_warnings:

        score += min(
            len(header_warnings) * 10,
            25
        )

        reasons.extend(header_warnings)


    # ==========================================
    # REMOVE DUPLICATE REASONS
    # ==========================================

    reasons = list(
        dict.fromkeys(reasons)
    )


    # ==========================================
    # FINAL SCORE
    # ==========================================

    score = min(
        score,
        100
    )


    # ==========================================
    # RISK LEVEL
    # ==========================================

    if score >= 60:

        risk_level = "HIGH"

    elif score >= 30:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    return score, risk_level, reasons