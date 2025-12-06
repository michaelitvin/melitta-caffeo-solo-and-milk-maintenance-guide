#!/usr/bin/env python3
"""Extract cleaning phase icons from annotated bounding boxes."""

import csv
import os
from PIL import Image
import numpy as np

LABELS_CSV = "assets/labels_melitta-caffeo-_2025-12-06-07-20-50.csv"
EXTRACTED_DIR = "assets/extracted_bboxes"
ICONS_DIR = "assets/icons"

# The source image is in assets/ folder
SOURCE_DIR = "assets"


def sanitize_filename(label):
    """Convert label to a safe filename."""
    return label.lower().replace(" ", "_").replace("/", "-")


def snap_to_content(img):
    """Remove excess whitespace by snapping to content borders."""
    # Convert to numpy array
    arr = np.array(img.convert("RGBA"))

    # Find non-white pixels (assuming white background ~255)
    # Check if pixel is not close to white
    threshold = 250
    mask = np.any(arr[:, :, :3] < threshold, axis=2)

    # Find bounding box of content
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)

    if not rows.any() or not cols.any():
        return img  # No content found, return original

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Add small padding
    padding = 2
    rmin = max(0, rmin - padding)
    rmax = min(arr.shape[0], rmax + padding + 1)
    cmin = max(0, cmin - padding)
    cmax = min(arr.shape[1], cmax + padding + 1)

    return img.crop((cmin, rmin, cmax, rmax))


def remove_background(img):
    """Remove white background and make it transparent."""
    img = img.convert("RGBA")
    arr = np.array(img)

    # Find white-ish pixels
    threshold = 240
    white_mask = np.all(arr[:, :, :3] > threshold, axis=2)

    # Set alpha to 0 for white pixels
    arr[white_mask, 3] = 0

    return Image.fromarray(arr)


def main():
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    os.makedirs(ICONS_DIR, exist_ok=True)

    images = {}

    # Read CSV and extract only the cleaning phase icons (last 3 rows)
    with open(LABELS_CSV, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Get last 3 rows (cleaning phase icons)
    cleaning_icons = rows[-3:]

    for row in cleaning_icons:
        label = row["label_name"]
        x = int(row["bbox_x"])
        y = int(row["bbox_y"])
        w = int(row["bbox_width"])
        h = int(row["bbox_height"])
        image_name = row["image_name"]

        # The image is in extracted/ folder
        img_path = os.path.join(SOURCE_DIR, image_name)

        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            continue

        if image_name not in images:
            images[image_name] = Image.open(img_path)
            print(f"Loaded: {image_name}")

        img = images[image_name]

        # Crop region
        cropped = img.crop((x, y, x + w, y + h))

        # Save raw extraction
        raw_filename = f"{sanitize_filename(label)}_raw.png"
        raw_path = os.path.join(EXTRACTED_DIR, raw_filename)
        cropped.save(raw_path, "PNG")
        print(f"  Extracted: {raw_filename} ({w}x{h})")

        # Snap to content borders
        snapped = snap_to_content(cropped)

        # Remove background
        processed = remove_background(snapped)

        # Save processed icon
        icon_filename = f"icon_clean_phase_{label.split()[0]}.png"
        icon_path = os.path.join(ICONS_DIR, icon_filename)
        processed.save(icon_path, "PNG")
        print(f"  Saved icon: {icon_filename}")

    for img in images.values():
        img.close()

    print(f"\nExtraction complete!")
    print(f"Raw extractions: {EXTRACTED_DIR}/")
    print(f"Processed icons: {ICONS_DIR}/")


if __name__ == "__main__":
    main()
