#!/usr/bin/env python3
"""Extract labeled regions from the Melitta Caffeo Solo & Milk manual images."""

import csv
import os
from PIL import Image

ASSETS_DIR = "assets"
LABELS_CSV = "assets/labels_melitta-caffeo-_2025-12-05-04-23-45.csv"
OUTPUT_DIR = "assets/icons"


def sanitize_filename(label):
    """Convert label to a safe filename."""
    return label.lower().replace(" ", "_").replace("/", "-")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load images into memory
    images = {}

    # Read CSV and extract regions
    with open(LABELS_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row["label_name"]
            x = int(row["bbox_x"])
            y = int(row["bbox_y"])
            w = int(row["bbox_width"])
            h = int(row["bbox_height"])
            image_name = row["image_name"]

            # Load image if not cached
            if image_name not in images:
                img_path = os.path.join(ASSETS_DIR, image_name)
                images[image_name] = Image.open(img_path)
                print(f"Loaded: {image_name}")

            img = images[image_name]

            # Crop region
            cropped = img.crop((x, y, x + w, y + h))

            # Save with sanitized filename
            filename = f"{sanitize_filename(label)}.png"
            output_path = os.path.join(OUTPUT_DIR, filename)

            # Handle duplicates by appending number
            counter = 1
            base_filename = filename
            while os.path.exists(output_path):
                filename = f"{sanitize_filename(label)}_{counter}.png"
                output_path = os.path.join(OUTPUT_DIR, filename)
                counter += 1

            cropped.save(output_path, "PNG")
            print(f"  Saved: {filename} ({w}x{h})")

    # Close images
    for img in images.values():
        img.close()

    print(f"\nExtraction complete! Icons saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
