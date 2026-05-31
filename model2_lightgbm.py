import re
import string
import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
import lightgbm as lgb

train = pd.read_csv("/mnt/user-data/uploads/train.csv")
test  = pd.read_csv("/mnt/user-data/uploads/test.csv")

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

word_vec = TfidfVectorizer(analyzer="word", ngram_range=(1, 2),
                           max_features=60000, sublinear_tf=True, min_df=2)
char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4),
                           max_features=40000, sublinear_tf=True, min_df=3)

Xtr = hstack([word_vec.fit_transform(X_train), char_vec.fit_transform(X_train)])
Xte = hstack([word_vec.transform(X_test),      char_vec.transform(X_test)])

params = {
    "objective":        "binary",
    "metric":           "binary_logloss",
    "learning_rate":    0.05,
    "num_leaves":       63,
    "min_child_samples":15,
    "feature_fraction": 0.7,
    "bagging_fraction": 0.8,
    "bagging_freq":     5,
    "lambda_l1":        0.2,
    "lambda_l2":        0.2,
    "is_unbalance":     True,
    "verbose":         -1,
    "seed":             42,
}

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
oof_f1 = []
test_preds = np.zeros(len(X_test))

for fold, (tr_idx, val_idx) in enumerate(skf.split(Xtr, y_train)):
    ds_tr  = lgb.Dataset(Xtr[tr_idx],  label=y_train[tr_idx])
    ds_val = lgb.Dataset(Xtr[val_idx], label=y_train[val_idx], reference=ds_tr)
    m = lgb.train(params, ds_tr, num_boost_round=400,
                  valid_sets=[ds_val],
                  callbacks=[lgb.early_stopping(30, verbose=False),
                             lgb.log_evaluation(period=-1)])
    val_prob = m.predict(Xtr[val_idx])
    val_pred = (val_prob >= 0.5).astype(int)
    oof_f1.append(f1_score(y_train[val_idx], val_pred))
    test_preds += m.predict(Xte) / 5

print(f"LightGBM             CV F1: {np.mean(oof_f1):.4f} ± {np.std(oof_f1):.4f}")

final_preds = (test_preds >= 0.5).astype(int)
out = pd.DataFrame({"id": test["id"].values, "target": final_preds})
out.to_csv("/home/claude/submission_v2.csv", index=False)
print("Saved submission_v2.csv")
