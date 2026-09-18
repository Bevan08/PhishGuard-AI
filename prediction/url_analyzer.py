import re
from urllib.parse import urlparse


# Common URL-shortening services
URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "rb.gy",
    "shorturl.at"
}


SUSPICIOUS_URL_KEYWORDS = {
    "login",
    "verify",
    "verification",
    "secure",
    "account",
    "update",
    "confirm",
    "password",
    "signin",
    "authenticate",
    "wallet",
    "payment",
    "banking"
}


def normalize_url(url):
    """
    Clean and normalize a URL before analysis.
    """

    url = url.strip()

    # Remove punctuation commonly attached to URLs in emails
    url = url.rstrip(".,!?;:)]}\"'")

    # urlparse needs a scheme to correctly identify the domain
    if url.startswith("www."):
        url = "http://" + url

    return url


def is_ip_address(hostname):
    """
    Check whether the hostname is an IPv4 address.
    """

    if not hostname:
        return False

    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    return bool(re.match(pattern, hostname))


def analyze_url(url):
    """
    Extract security-related features from a URL.
    """

    url = normalize_url(url)

    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    domain = hostname.lower()

    # Remove main domain and TLD to estimate subdomains
    domain_parts = domain.split(".") if domain else []

    if len(domain_parts) >= 2:
        subdomain_count = len(domain_parts) - 2
    else:
        subdomain_count = 0

    # Count special characters
    special_characters = re.findall(
        r"[^a-zA-Z0-9]",
        url
    )

    # Suspicious keywords
    suspicious_keywords = []

    for keyword in SUSPICIOUS_URL_KEYWORDS:
        if keyword in url.lower():
            suspicious_keywords.append(keyword)

    # Check URL shortener
    is_shortener = domain in URL_SHORTENERS

    # Check unusual port
    has_port = parsed.port is not None

    features = {
        "url": url,

        # Basic URL properties
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(parsed.path),

        # Character statistics
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": sum(char.isdigit() for char in url),
        "num_special_characters": len(special_characters),

        # Domain structure
        "num_subdomains": subdomain_count,

        # Security indicators
        "uses_https": parsed.scheme.lower() == "https",
        "has_ip_address": is_ip_address(domain),
        "has_at_symbol": "@" in url,
        "has_punycode": "xn--" in domain,
        "has_port": has_port,

        # Suspicious patterns
        "is_shortened": is_shortener,
        "suspicious_keywords": suspicious_keywords
    }

    warnings = []

    if features["url_length"] > 100:
        warnings.append("Unusually long URL")

    if features["domain_length"] > 50:
        warnings.append("Unusually long domain")

    if features["num_subdomains"] >= 3:
        warnings.append("Large number of subdomains")

    if features["has_ip_address"]:
        warnings.append("URL uses an IP address instead of a domain name")

    if features["has_at_symbol"]:
        warnings.append("URL contains @ symbol")

    if features["has_punycode"]:
        warnings.append("Domain uses punycode")

    if features["has_port"]:
        warnings.append("URL uses a custom port")

    if features["is_shortened"]:
        warnings.append("URL uses a shortening service")

    if features["suspicious_keywords"]:
        warnings.append(
            "Suspicious keywords found: "
            + ", ".join(features["suspicious_keywords"])
        )

    features["warnings"] = warnings

    return features