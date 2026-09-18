from header_analyzer import analyze_headers


email = """
From: PayPal Security <security@paypal.com>
Reply-To: verify-account@gmail.com
Return-Path: attacker@gmail.com
Authentication-Results: spf=fail; dkim=fail; dmarc=fail

Subject: URGENT - Verify Your Account

Your account has been flagged.
Please verify your identity immediately.
"""


result = analyze_headers(email)


print("=" * 60)
print("EMAIL HEADER ANALYSIS")
print("=" * 60)

print()

print("From:", result["from"])
print("Reply-To:", result["reply_to"])
print("Return-Path:", result["return_path"])
print(
    "Authentication:",
    result["authentication_results"]
)

print()

print("Warnings:")

for warning in result["warnings"]:
    print("⚠️", warning)

print("=" * 60)