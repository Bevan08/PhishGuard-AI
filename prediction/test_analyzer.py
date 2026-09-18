import sys
import os

# Add project root to Python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from prediction.phishing_analyzer import analyze_email


email = """
URGENT!

Your bank account has been suspended.

Please verify your account immediately:
http://192.168.1.10/login

Enter your password and OTP to restore access.
"""


result = analyze_email(email)


print("\n========== EMAIL ANALYSIS ==========\n")

print("URLs:")
for url in result["urls"]:
    print("-", url)


print("\nURL Warnings:")
for warning in result["url_reasons"]:
    print("-", warning)


print("\nUrgency Words:")
print(result["urgency_words"])


print("\nCredential Words:")
print(result["credential_words"])


print("\nFinancial Words:")
print(result["financial_words"])


print("\nURL Details:")

for details in result["url_details"]:

    print("\n----------------------------")

    for key, value in details.items():

        if key != "warnings":
            print(f"{key}: {value}")