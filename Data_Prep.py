import os
import random
from datasets import load_dataset
from PIL import Image

# ── Config ────────────────────────────────────────────────────
TRAIN_RATIO = 0.80          # 80% train, 20% val
SEED        = 42            # reproducible shuffle
OUTPUT_ROOT = "datasets/receipts"

# ── Directory structure ───────────────────────────────────────
for split in ["train", "val"]:
    os.makedirs(f"{OUTPUT_ROOT}/images/{split}", exist_ok=True)
    os.makedirs(f"{OUTPUT_ROOT}/labels/{split}", exist_ok=True)

# ── Load SROIE ────────────────────────────────────────────────
print("Fetching SROIE dataset from HuggingFace...")
dataset = load_dataset("jsdnrs/ICDAR2019-SROIE", split="train")

# ── Shuffle + split ───────────────────────────────────────────
indices = list(range(len(dataset)))
random.seed(SEED)
random.shuffle(indices)

split_point  = int(len(indices) * TRAIN_RATIO)
train_indices = indices[:split_point]
val_indices   = indices[split_point:]

print(f"Total images : {len(dataset)}")
print(f"Train        : {len(train_indices)}  ({TRAIN_RATIO*100:.0f}%)")
print(f"Val          : {len(val_indices)}    ({(1-TRAIN_RATIO)*100:.0f}%)")

# ── Save images + labels ──────────────────────────────────────
def write_sample(item, split: str, idx: int):
    """Save one image and its YOLO label file."""
    img: Image.Image = item["image"]
    img_path   = f"{OUTPUT_ROOT}/images/{split}/receipt_{idx}.jpg"
    label_path = f"{OUTPUT_ROOT}/labels/{split}/receipt_{idx}.txt"

    img.save(img_path, "JPEG", quality=95)

    # Whole-image bounding box (entire receipt = class 0)
    # YOLO format: <class> <x_center> <y_center> <width> <height>  (all normalised 0-1)
    with open(label_path, "w") as f:
        f.write("0 0.5 0.5 1.0 1.0\n")

for idx in train_indices:
    write_sample(dataset[idx], "train", idx)

for idx in val_indices:
    write_sample(dataset[idx], "val", idx)

print(f"\nDone! Dataset saved to '{OUTPUT_ROOT}/'")
print("Next step: run train.py")
