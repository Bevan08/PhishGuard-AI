from url_analyzer import analyze_url


test_urls = [
    "https://www.google.com",
    "http://192.168.1.10/login",
    "https://secure-login-account-verify.example.com/password",
    "https://bit.ly/abc123"
]


for url in test_urls:

    print("\n" + "=" * 60)
    print("URL:", url)

    result = analyze_url(url)

    print("\nFeatures:")

    for key, value in result.items():
        if key != "warnings":
            print(f"{key}: {value}")

    print("\nWarnings:")

    if result["warnings"]:
        for warning in result["warnings"]:
            print("-", warning)
    else:
        print("No obvious warning indicators.")