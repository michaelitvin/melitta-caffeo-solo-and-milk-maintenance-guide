#!/usr/bin/env python3
"""Prepare clean icons from extracted bounding boxes."""

import os
from PIL import Image

ASSETS_DIR = "assets"
EXTRACTED_DIR = "assets/extracted_bboxes"
ICONS_DIR = "assets/icons"


def remove_white_background(img, threshold=250):
    """Convert white background to transparent."""
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        # If pixel is close to white, make it transparent
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def auto_crop(img):
    """Auto-crop to content, removing transparent/white borders."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def snap_to_edges(img, threshold=250):
    """Auto-crop to snap to content edges, removing white/light gray borders."""
    # Convert to RGB for analysis
    rgb_img = img.convert("RGB")
    pixels = rgb_img.load()
    w, h = img.size

    # Find bounds of non-white content
    left, top, right, bottom = w, h, 0, 0

    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            # Check if pixel is not white/near-white
            if r < threshold or g < threshold or b < threshold:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    # Add small padding
    padding = 5
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(w, right + padding)
    bottom = min(h, bottom + padding)

    if right > left and bottom > top:
        return img.crop((left, top, right, bottom))
    return img


def main():
    os.makedirs(ICONS_DIR, exist_ok=True)

    # Define which icons we need and their source
    # Format: output_name -> (source_file, needs_transparency, snap_edges, description)
    icons_to_extract = {
        # Display indicator icons (from light_icon_*.png)
        "icon_power": ("light_icon.png", True, False, "Power/Ready"),
        "icon_filter": ("light_icon_1.png", True, False, "Water filter"),
        "icon_water": ("light_icon_2.png", True, False, "Water reservoir"),
        "icon_drip_tray": ("light_icon_3.png", True, False, "Drip tray"),
        "icon_beans": ("light_icon_4.png", True, False, "Bean strength"),
        "icon_clean": ("light_icon_5.png", True, False, "Cleaning"),
        "icon_descale": ("light_icon_6.png", True, False, "Descaling"),
        "icon_steam": ("light_icon_7.png", True, False, "Steam ready"),

        # Button icons
        "btn_power": ("3_on-off.png", True, False, "ON/OFF button"),
        "btn_coffee": ("5_coffee_dispensing.png", True, False, "Coffee button"),
        "btn_strength": ("6_coffee_strength.png", True, False, "Strength button"),
        "btn_steam": ("9_steam_dispensing.png", True, False, "Steam button"),

        # Component diagrams (snap to edges, keep letter labels)
        "diagram_brewing_unit_remove": ("b.png", False, True, "Brewing unit removal"),
        "diagram_brewing_unit_clean_tab": ("c.png", False, True, "Cleaning tab placement"),
        "diagram_brewing_chamber": ("d.png", False, True, "Brewing chamber"),
        "diagram_control_panel": ("e.png", False, True, "Control panel"),
        "diagram_steam_pipe_twist": ("f.png", False, True, "Steam pipe twist off"),
        "diagram_steam_pipe_parts": ("g.png", False, True, "Steam pipe parts"),
        "diagram_nozzle_clean": ("h.png", False, True, "Nozzle cleaning"),
        "diagram_descale_setup": ("j.png", False, True, "Descaling setup"),
        "diagram_steam_positions": ("k.png", False, True, "Steam pipe positions"),
        "diagram_machine": ("a.png", False, True, "Machine overview"),
    }

    for output_name, (source_file, needs_transparency, snap_edges, desc) in icons_to_extract.items():
        source_path = os.path.join(EXTRACTED_DIR, source_file)
        if not os.path.exists(source_path):
            print(f"  SKIP: {source_file} not found")
            continue

        img = Image.open(source_path)

        # Snap to edges (auto-crop white borders) if needed
        if snap_edges:
            img = snap_to_edges(img)

        if needs_transparency:
            img = remove_white_background(img)
            img = auto_crop(img)

        output_path = os.path.join(ICONS_DIR, f"{output_name}.png")
        img.save(output_path, "PNG")
        print(f"  Saved: {output_name}.png ({img.size[0]}x{img.size[1]}) - {desc}")

    print(f"\nIcons prepared in {ICONS_DIR}/")


if __name__ == "__main__":
    main()
