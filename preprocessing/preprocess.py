import pandas as pd
import re


# Load dataset
data = pd.read_csv("dataset/emails.csv")


print("Original dataset size:")
print(len(data))


# Remove missing values
data = data.dropna(subset=["text", "label"])


# Remove duplicate emails
data = data.drop_duplicates(subset=["text"])


# Convert email text to lowercase
data["text"] = data["text"].str.lower()


# Remove HTML tags
def remove_html(text):
    return re.sub(r"<.*?>", " ", text)


data["text"] = data["text"].apply(remove_html)


# Remove URLs
def remove_urls(text):
    return re.sub(r"http\S+|www\S+|https\S+", " ", text)


data["text"] = data["text"].apply(remove_urls)


# Remove special characters
def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


data["text"] = data["text"].apply(clean_text)


# Remove empty emails
data = data[data["text"].str.strip() != ""]


# Shuffle dataset
data = data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# Save cleaned dataset
data.to_csv(
    "dataset/cleaned_emails.csv",
    index=False
)


print("\nCleaning completed!")

print("\nClean dataset size:")
print(len(data))


print("\nClass distribution:")
print(data["label"].value_counts())


print("\nCleaned dataset saved as:")
print("dataset/cleaned_emails.csv")