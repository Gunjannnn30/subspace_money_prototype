import re
import string
import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

train = pd.read_csv("/mnt/user-data/uploads/train.csv")
test  = pd.read_csv("/mnt/user-data/uploads/test.csv")

# Note: train.csv has no id column, so we use row index as id
train["id"] = range(len(train))

def clean(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", "url", text)
    text = re.sub(r"@\w+", "user", text)
    text = re.sub(r"#(\w+)", r"\1", text)
    text = re.sub(r"\d+", "num", text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

train["clean"] = train["text"].apply(clean)
test["clean"]  = test["text"].apply(clean)

X_train = train["clean"].values
y_train = train["target"].values
X_test  = test["clean"].values

word_vec = TfidfVectorizer(analyzer="word", ngram_range=(1, 3),
                           max_features=70000, sublinear_tf=True, min_df=2)
char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5),
                           max_features=50000, sublinear_tf=True, min_df=3)

Xtr = hstack([word_vec.fit_transform(X_train), char_vec.fit_transform(X_train)])
Xte = hstack([word_vec.transform(X_test),      char_vec.transform(X_test)])

model = LogisticRegression(C=4.0, max_iter=1000, solver="saga",
                           class_weight="balanced", random_state=7)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=7)
scores = cross_val_score(model, Xtr, y_train, cv=cv, scoring="f1")
print(f"Logistic Regression  CV F1: {scores.mean():.4f} ± {scores.std():.4f}")

model.fit(Xtr, y_train)
preds = model.predict(Xte)

out = pd.DataFrame({"id": test["id"].values, "target": preds})
out.to_csv("/home/claude/submission_v1.csv", index=False)
print("Saved submission_v1.csv")
