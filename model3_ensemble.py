import re
import string
import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
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

word_vec = TfidfVectorizer(analyzer="word", ngram_range=(1, 3),
                           max_features=80000, sublinear_tf=True, min_df=2)
char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5),
                           max_features=60000, sublinear_tf=True, min_df=2)

Xtr = hstack([word_vec.fit_transform(X_train), char_vec.fit_transform(X_train)])
Xte = hstack([word_vec.transform(X_test),      char_vec.transform(X_test)])

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=11)

# --- Logistic Regression ---
lr = LogisticRegression(C=5.0, max_iter=1000, solver="saga",
                        class_weight="balanced", random_state=11)
lr_f1 = []
for tr_idx, val_idx in skf.split(Xtr, y_train):
    lr.fit(Xtr[tr_idx], y_train[tr_idx])
    lr_f1.append(f1_score(y_train[val_idx], lr.predict(Xtr[val_idx])))
print(f"  LR                 CV F1: {np.mean(lr_f1):.4f}")
lr.fit(Xtr, y_train)
pred_lr = lr.predict(Xte)

# --- LinearSVC ---
svc = CalibratedClassifierCV(
    LinearSVC(C=0.5, max_iter=2000, class_weight="balanced", random_state=11), cv=3)
svc_f1 = []
for tr_idx, val_idx in skf.split(Xtr, y_train):
    svc.fit(Xtr[tr_idx], y_train[tr_idx])
    svc_f1.append(f1_score(y_train[val_idx], svc.predict(Xtr[val_idx])))
print(f"  LinearSVC          CV F1: {np.mean(svc_f1):.4f}")
svc.fit(Xtr, y_train)
pred_svc = svc.predict(Xte)

# --- LightGBM averaged over folds ---
params = {
    "objective": "binary", "metric": "binary_logloss",
    "learning_rate": 0.05, "num_leaves": 63,
    "min_child_samples": 15, "feature_fraction": 0.7,
    "bagging_fraction": 0.8, "bagging_freq": 5,
    "is_unbalance": True, "verbose": -1, "seed": 11,
}
lgb_preds = np.zeros(len(X_test))
lgb_f1 = []
for tr_idx, val_idx in skf.split(Xtr, y_train):
    ds_tr  = lgb.Dataset(Xtr[tr_idx],  label=y_train[tr_idx])
    ds_val = lgb.Dataset(Xtr[val_idx], label=y_train[val_idx], reference=ds_tr)
    m = lgb.train(params, ds_tr, num_boost_round=400,
                  valid_sets=[ds_val],
                  callbacks=[lgb.early_stopping(30, verbose=False),
                             lgb.log_evaluation(period=-1)])
    lgb_f1.append(f1_score(y_train[val_idx],
                           (m.predict(Xtr[val_idx]) >= 0.5).astype(int)))
    lgb_preds += m.predict(Xte) / 5
pred_lgb = (lgb_preds >= 0.5).astype(int)
print(f"  LightGBM           CV F1: {np.mean(lgb_f1):.4f}")

# --- Majority vote ---
votes      = pred_lr.astype(int) + pred_svc.astype(int) + pred_lgb
final_pred = (votes >= 2).astype(int)
print(f"\n  Ensemble (majority vote) — predictions saved.")

out = pd.DataFrame({"id": test["id"].values, "target": final_pred})
out.to_csv("/home/claude/submission_v3.csv", index=False)
print("Saved submission_v3.csv")
