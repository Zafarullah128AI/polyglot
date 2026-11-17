"""Standalone evaluation for Polyglot — prints headline metrics and writes
evaluation.json (used for the exhibition report).

Headline metrics come from a stratified 80/20 hold-out split (seed 42).
Accuracy by snippet length comes from 5-fold cross-validated predictions
on the full dataset.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from model import Engine  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))


def main():
    eng = Engine()
    ev = eng.evaluation
    print(f"Dataset: {len(eng.df)} snippets, {len(ev['labels'])} languages")
    print(f"Hold-out: train {ev['train_size']} / test {ev['test_size']}")
    print()
    print("Model comparison (hold-out):")
    for name, m in sorted(ev["models"].items(), key=lambda kv: -kv[1]["accuracy"]):
        print(f"  {name:22s} acc {m['accuracy']:.4f}  prec {m['precision']:.4f}  "
              f"rec {m['recall']:.4f}  f1 {m['f1']:.4f}")
    print(f"\nBest model: {ev['best_model']}")
    print("\nAccuracy by snippet length (5-fold CV):")
    for name, buckets in ev["by_length"].items():
        parts = "  ".join(f"{b}: {v['accuracy']:.4f} (n={v['n']})" for b, v in buckets.items())
        print(f"  {name:22s} {parts}")
    print("\nPer-language (best model):")
    for row in ev["per_language"]:
        print(f"  {row['language']:12s} prec {row['precision']:.3f}  "
              f"rec {row['recall']:.3f}  f1 {row['f1']:.3f}  (n={row['support']})")
    out = os.path.join(BASE, "evaluation.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(ev, f, indent=2)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
