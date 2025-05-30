import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def classify_email(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]
