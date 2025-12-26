from datasets import load_dataset
import pandas as pd
import re
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
STOP = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP]
    return " ".join(tokens)

# Load dataset
ds = load_dataset("ag_news")
df = pd.DataFrame(ds['train'])
df = df.rename(columns={'text': 'article', 'label': 'label'})
label_map = {0: 'World', 1: 'Sports', 2: 'Business', 3: 'Sci/Tech'}
df['category'] = df['label'].map(label_map)

X = df['article'].apply(clean_text)
y = df['category']

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

tfidf = TfidfVectorizer(max_features=30000, ngram_range=(1,2))
X_train_tfidf = tfidf.fit_transform(X_train)
X_val_tfidf = tfidf.transform(X_val)

clf = MultinomialNB(alpha=0.1)
clf.fit(X_train_tfidf, y_train)

pred = clf.predict(X_val_tfidf)
print("Accuracy:", accuracy_score(y_val, pred))
print(classification_report(y_val, pred))

joblib.dump(tfidf, "tfidf_vectorizer.joblib")
joblib.dump(clf, "news_clf_nb.joblib")
