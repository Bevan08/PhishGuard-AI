from sender_analyzer import analyze_senders


email = """
From: security@secure-login-account-example.com

URGENT!

Your account requires verification.

Please login and confirm your password.
"""


results = analyze_senders(email)


print("\n==============================")
print("SENDER ANALYZER")
print("==============================")


print("\nEmail addresses found:")

for sender in results["senders"]:
    print(sender)


print("\nSender warnings:")

if results["sender_reasons"]:

    for reason in results["sender_reasons"]:
        print("⚠️", reason)

else:

    print("No sender warnings detected.")