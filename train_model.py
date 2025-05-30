import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib
from pii_masker import mask_entities

# Load the dataset
df = pd.read_csv("support_emails.csv")

print("Initial dataset size:", len(df))
print("Missing email_text:", df['email_text'].isnull().sum())
print("Missing category:", df['category'].isnull().sum())

# Drop rows where email_text or category is missing
df = df.dropna(subset=['email_text', 'category'])

print("Size after dropping missing email_text/category:", len(df))

# Mask PII entities safely
def safe_mask(x):
    result = mask_entities(x)[0]
    if result is None or result == '':
        return ''
    return result

df['masked_text'] = df['email_text'].apply(safe_mask)

print("Number of empty masked_text rows:", (df['masked_text'] == '').sum())

# Optional: Print some examples with empty masked_text to debug
print("\nExamples of empty masked_text rows:")
print(df.loc[df['masked_text'] == '', ['email_text', 'masked_text']].head())

# Drop rows with empty masked_text or empty category
df = df[(df['masked_text'] != '') & (df['category'] != '')]

print("Size after dropping empty masked_text and category:", len(df))

# Show a few rows after cleaning
print("\nSample rows after cleaning:")
print(df.head())

# Prepare features and labels
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['masked_text'])
y = df['category']

print("Feature matrix shape:", X.shape)
print("Number of labels:", len(y))

# Check if dataset is big enough for train/test split
if len(df) < 2:
    raise ValueError(f"Not enough samples ({len(df)}) to split into train and test sets.")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = SVC(probability=True)
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Training completed and models saved successfully.")
