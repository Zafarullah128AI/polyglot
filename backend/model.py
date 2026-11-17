"""Polyglot model engine: 3 text-classification models that identify the
programming language of a code snippet.

Features: character n-grams (3-5, inside word boundaries) — these capture
the punctuation and keyword shapes that make languages look different
(def/end, public class, #include, <?php, fn/let, package main, ...).

Models
  1. Logistic Regression  (char TF-IDF + LR)
  2. Naive Bayes         (char TF-IDF + MultinomialNB)
  3. Linear SVM          (char TF-IDF + LinearSVC, calibrated for probabilities)

Evaluation
  - Headline metrics: stratified 80/20 hold-out split (seed 42).
  - Accuracy by snippet length: 5-fold cross-validated predictions on the
    full dataset, grouped by length bucket (short 1-3 lines,
    medium 4-10 lines, long 11+ lines).
"""
import os

import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE, "data.csv")

LANGUAGES = ["C", "C#", "C++", "Go", "Java", "JavaScript", "PHP", "Python", "Rust", "TypeScript"]
BUCKETS = ["short", "medium", "long"]


def make_vectorizer():
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=8000)


def make_models():
    return {
        "Logistic Regression": Pipeline([
            ("tfidf", make_vectorizer()),
            ("clf", LogisticRegression(max_iter=2000, C=10)),
        ]),
        "Naive Bayes": Pipeline([
            ("tfidf", make_vectorizer()),
            ("clf", MultinomialNB(alpha=0.1)),
        ]),
        "Linear SVM": Pipeline([
            ("tfidf", make_vectorizer()),
            ("clf", CalibratedClassifierCV(LinearSVC(C=1.0), cv=3)),
        ]),
    }


def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["language", "code"])
    df["code"] = df["code"].astype(str)
    return df


def length_bucket(code: str) -> str:
    lines = code.count("\n") + 1
    if lines <= 3:
        return "short"
    if lines <= 10:
        return "medium"
    return "long"


class Engine:
    def __init__(self):
        self.df = load_data()
        self.models = make_models()
        self.trained = {}
        self.evaluation = None
        self.train_all()

    def train_all(self):
        X = self.df["code"].tolist()
        y = self.df["language"].tolist()
        for name, pipe in self.models.items():
            pipe.fit(X, y)
            self.trained[name] = pipe
        self.evaluation = self._evaluate()

    def retrain(self):
        self.df = load_data()
        self.models = make_models()
        self.train_all()

    def _proba(self, pipe, code: str):
        classes = list(pipe.classes_)
        proba = pipe.predict_proba([code])[0]
        order = sorted(range(len(classes)), key=lambda i: proba[i], reverse=True)
        return [{"language": classes[i], "probability": float(proba[i])} for i in order]

    def predict(self, code: str, model_name: str = None):
        """Predict with one model (default: best model) or all models."""
        name = model_name or self.best_model()
        pipe = self.trained[name]
        top = self._proba(pipe, code)
        return {
            "model": name,
            "language": top[0]["language"],
            "confidence": top[0]["probability"],
            "top3": top[:3],
        }

    def predict_all(self, code: str):
        votes = {}
        results = {}
        for name, pipe in self.trained.items():
            top = self._proba(pipe, code)
            results[name] = {
                "language": top[0]["language"],
                "confidence": top[0]["probability"],
                "top3": top[:3],
            }
            votes[top[0]["language"]] = votes.get(top[0]["language"], 0) + 1
        winner = max(votes, key=votes.get)
        return {"winner": winner, "votes": votes, "models": results}

    def best_model(self):
        ev = self.evaluation["models"]
        return max(ev, key=lambda m: ev[m]["accuracy"])

    def _evaluate(self):
        df = self.df
        X = df["code"].tolist()
        y = df["language"].tolist()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        labels = sorted(set(y))
        models_eval = {}
        for name, pipe in self.models.items():
            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            acc = accuracy_score(y_test, pred)
            prec, rec, f1, _ = precision_recall_fscore_support(
                y_test, pred, average="macro", zero_division=0
            )
            models_eval[name] = {
                "accuracy": round(float(acc), 4),
                "precision": round(float(prec), 4),
                "recall": round(float(rec), 4),
                "f1": round(float(f1), 4),
                "test_size": len(y_test),
            }
        # Per-language report + confusion matrix for the best model.
        best = max(models_eval, key=lambda m: models_eval[m]["accuracy"])
        best_pipe = self.models[best]
        pred = best_pipe.predict(X_test)
        prec, rec, f1, support = precision_recall_fscore_support(
            y_test, pred, labels=labels, zero_division=0
        )
        per_language = [
            {
                "language": lab,
                "precision": round(float(p), 4),
                "recall": round(float(r), 4),
                "f1": round(float(f), 4),
                "support": int(s),
            }
            for lab, p, r, f, s in zip(labels, prec, rec, f1, support)
        ]
        cm = confusion_matrix(y_test, pred, labels=labels).tolist()
        # Accuracy by snippet length (5-fold CV predictions on the full set).
        by_length = {}
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        for name, pipe in self.models.items():
            cv_pred = cross_val_predict(pipe, X, y, cv=skf)
            entry = {}
            for b in BUCKETS:
                idx = [i for i, row in enumerate(df.itertuples()) if row.length_bucket == b]
                if idx:
                    acc_b = accuracy_score([y[i] for i in idx], [cv_pred[i] for i in idx])
                    entry[b] = {"accuracy": round(float(acc_b), 4), "n": len(idx)}
            by_length[name] = entry
        return {
            "models": models_eval,
            "best_model": best,
            "labels": labels,
            "per_language": per_language,
            "confusion_matrix": cm,
            "by_length": by_length,
            "test_size": len(y_test),
            "train_size": len(y_train),
        }

    def dataset_stats(self):
        counts = self.df["language"].value_counts().to_dict()
        buckets = self.df["length_bucket"].value_counts().to_dict()
        return {
            "total": int(len(self.df)),
            "languages": sorted(counts.keys()),
            "per_language": {k: int(counts.get(k, 0)) for k in sorted(counts)},
            "per_bucket": {b: int(buckets.get(b, 0)) for b in BUCKETS},
        }

    def samples(self, language: str, n: int = 3):
        sub = self.df[self.df["language"] == language]
        return sub["code"].head(n).tolist()

    def add_snippet(self, language: str, code: str):
        if language not in LANGUAGES:
            raise ValueError(f"Unknown language: {language}")
        code = code.strip("\n")
        if len(code.strip()) < 3:
            raise ValueError("Snippet is too short.")
        lines = code.count("\n") + 1
        row = {
            "language": language,
            "code": code,
            "lines": lines,
            "chars": len(code),
            "length_bucket": "short" if lines <= 3 else ("medium" if lines <= 10 else "long"),
        }
        new = pd.DataFrame([row])
        df = pd.concat([self.df, new], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        self.retrain()
        return row

    def add_csv(self, path: str):
        new = pd.read_csv(path)
        new = new.dropna(subset=["language", "code"])
        new = new[new["language"].isin(LANGUAGES)]
        if len(new) == 0:
            raise ValueError("No valid rows (need columns language,code with a known language).")
        new["code"] = new["code"].astype(str).str.strip("\n")
        new["lines"] = new["code"].apply(lambda c: c.count("\n") + 1)
        new["chars"] = new["code"].apply(len)
        new["length_bucket"] = new["lines"].apply(
            lambda n: "short" if n <= 3 else ("medium" if n <= 10 else "long")
        )
        df = pd.concat([self.df, new[["language", "code", "lines", "chars", "length_bucket"]]],
                       ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        self.retrain()
        return len(new)
