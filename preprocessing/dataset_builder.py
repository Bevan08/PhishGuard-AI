import os
import tarfile
import pandas as pd
from email import policy
from email.parser import BytesParser


RAW_FOLDER = "../dataset/raw"
EXTRACT_FOLDER = "../dataset/extracted"
OUTPUT_FILE = "../dataset/emails.csv"


def extract_archive(archive_path, extract_path):

    print(f"Extracting: {archive_path}")

    with tarfile.open(archive_path, "r") as tar:
        tar.extractall(extract_path)

    print("Extraction completed.")


def extract_email_text(file_path):

    try:

        with open(file_path, "rb") as file:
            message = BytesParser(
                policy=policy.default
            ).parse(file)

        body = message.get_body(
            preferencelist=("plain", "html")
        )

        if body:
            return body.get_content()

        return ""

    except Exception:
        return ""


def process_emails(folder, label):

    emails = []

    for root, directories, files in os.walk(folder):

        for filename in files:

            file_path = os.path.join(
                root,
                filename
            )

            text = extract_email_text(
                file_path
            )

            if text.strip():

                emails.append({
                    "text": text,
                    "label": label
                })

    return emails


def main():

    print("Starting dataset builder...")

    os.makedirs(
        EXTRACT_FOLDER,
        exist_ok=True
    )

    ham_archive = os.path.join(
        RAW_FOLDER,
        "20030228_easy_ham_2.tar.bz2"
    )

    spam_archive = os.path.join(
        RAW_FOLDER,
        "20050311_spam_2.tar.bz2"
    )

    # Extract HAM
    extract_archive(
        ham_archive,
        EXTRACT_FOLDER
    )

    # Extract SPAM
    extract_archive(
        spam_archive,
        EXTRACT_FOLDER
    )

    print("Reading legitimate emails...")

    ham_emails = process_emails(
        os.path.join(
            EXTRACT_FOLDER,
            "easy_ham_2"
        ),
        0
    )

    print(
        f"Legitimate emails found: {len(ham_emails)}"
    )

    print("Reading spam emails...")

    spam_emails = process_emails(
        os.path.join(
            EXTRACT_FOLDER,
            "spam_2"
        ),
        1
    )

    print(
        f"Spam emails found: {len(spam_emails)}"
    )

    all_emails = ham_emails + spam_emails

    df = pd.DataFrame(all_emails)

    df = df.dropna()

    df = df[
        df["text"].str.strip() != ""
    ]

    df = df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n-----------------------------")
    print("Dataset created successfully!")
    print("-----------------------------")

    print(
        f"\nTotal emails: {len(df)}"
    )

    print("\nClass distribution:")
    print(
        df["label"].value_counts()
    )

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()