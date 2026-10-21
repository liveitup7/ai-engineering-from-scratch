# Lesson: phases/00-setup-and-tooling/09-data-management/docs/en.md
# Exercises 1-4: Inspect, stream, export, and split datasets.
# Reference: https://huggingface.co/datasets/nyu-mll/glue
# Reference: https://huggingface.co/docs/datasets/stream
# Run: python phases/00-setup-and-tooling/09-data-management/code/data_practice.py

from pathlib import Path
from time import perf_counter

from datasets import load_dataset

dataset = load_dataset("nyu-mll/glue", "mrpc", split="train")
print(dataset)

for number, example in enumerate(dataset.select(range(5)), start=1):
    print(f"\nExample {number}:")
    print(example)

# Exercise 2: Count C4 examples streamed in about ten seconds.
print("\nExercise 2: C4 streaming")

stream = load_dataset("allenai/c4", "en", split="train", streaming=True)

count = 0
started = perf_counter()

for example in stream:
    count += 1
    if perf_counter() - started >= 10:
        break

elapsed = perf_counter() - started
print(f"Processed {count:,} examples in {elapsed:.2f} seconds.")

# Exercise 3: Export the same dataset to CSV and Parquet and compare sizes.
print("\nExercise 3: CSV and Parquet file sizes")

imdb = load_dataset("stanfordnlp/imdb", split="train")
output_dir = Path("data/data-management")
output_dir.mkdir(parents=True, exist_ok=True)

csv_path = output_dir / "imdb_train.csv"
parquet_path = output_dir / "imdb_train.parquet"
imdb.to_csv(str(csv_path))
imdb.to_parquet(str(parquet_path))

csv_bytes = csv_path.stat().st_size
parquet_bytes = parquet_path.stat().st_size
reduction = (1 - parquet_bytes / csv_bytes) * 100

print(f"Rows exported: {len(imdb):,}")
print(f"CSV: {csv_bytes:,} bytes")
print(f"Parquet: {parquet_bytes:,} bytes")
print(f"Parquet uses {reduction:.1f}% less disk space than CSV for this dataset.")

# Exercise 4: Create and verify reproducible 70/15/15 splits.
print("\nExercise 4: Reproducible 70/15/15 splits")


def make_practice_splits(source, seed=42):
    train_holdout = source.train_test_split(test_size=0.3, seed=seed)
    validation_test = train_holdout["test"].train_test_split(test_size=0.5, seed=seed)
    return {
        "train": train_holdout["train"],
        "validation": validation_test["train"],
        "test": validation_test["test"],
    }


indexed_imdb = imdb.add_column("row_id", list(range(len(imdb))))
splits = make_practice_splits(indexed_imdb, seed=42)
repeated_splits = make_practice_splits(indexed_imdb, seed=42)
expected_sizes = {"train": 17_500, "validation": 3_750, "test": 3_750}
seen_row_ids = set()

for name, subset in splits.items():
    row_ids = list(subset["row_id"])
    assert len(subset) == expected_sizes[name], f"Unexpected {name} size"
    assert seen_row_ids.isdisjoint(row_ids), f"Overlapping rows in {name}"
    assert row_ids == list(repeated_splits[name]["row_id"]), f"{name} changed on repeat"
    seen_row_ids.update(row_ids)
    print(f"{name.capitalize()}: {len(subset):,} ({len(subset) / len(imdb):.0%})")

assert seen_row_ids == set(range(len(imdb))), "Some original rows are missing"
print("Verified: expected sizes, no overlapping or missing rows, and repeatable splits.")
