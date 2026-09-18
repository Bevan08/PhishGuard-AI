import re


def extract_email_address(value):
    match = re.search(
        r'[\w.-]+@[\w.-]+\.\w+',
        value
    )

    if match:
        return match.group(0)

    return None


def analyze_headers(email_text):

    results = {
        "from": None,
        "reply_to": None,
        "return_path": None,
        "authentication_results": None,
        "warnings": []
    }

    # FROM
    from_match = re.search(
        r'^From:\s*(.+)$',
        email_text,
        re.IGNORECASE | re.MULTILINE
    )

    if from_match:
        results["from"] = extract_email_address(
            from_match.group(1).strip()
        )

    # REPLY-TO
    reply_match = re.search(
        r'^Reply-To:\s*(.+)$',
        email_text,
        re.IGNORECASE | re.MULTILINE
    )

    if reply_match:
        results["reply_to"] = extract_email_address(
            reply_match.group(1).strip()
        )

    # RETURN-PATH
    return_match = re.search(
        r'^Return-Path:\s*(.+)$',
        email_text,
        re.IGNORECASE | re.MULTILINE
    )

    if return_match:
        results["return_path"] = extract_email_address(
            return_match.group(1).strip()
        )

    # AUTHENTICATION RESULTS
    auth_match = re.search(
        r'^Authentication-Results:\s*(.+)$',
        email_text,
        re.IGNORECASE | re.MULTILINE
    )

    if auth_match:
        results["authentication_results"] = (
            auth_match.group(1).strip()
        )

    # FROM / REPLY-TO MISMATCH
    if results["from"] and results["reply_to"]:

        from_domain = results["from"].split("@")[-1].lower()
        reply_domain = results["reply_to"].split("@")[-1].lower()

        if from_domain != reply_domain:
            results["warnings"].append(
                "From and Reply-To domains do not match"
            )

    # AUTHENTICATION WARNINGS
    auth = results["authentication_results"]

    if auth:

        auth_lower = auth.lower()

        if "spf=fail" in auth_lower:
            results["warnings"].append(
                "SPF authentication failed"
            )

        if "dkim=fail" in auth_lower:
            results["warnings"].append(
                "DKIM authentication failed"
            )

        if "dmarc=fail" in auth_lower:
            results["warnings"].append(
                "DMARC authentication failed"
            )

    return results