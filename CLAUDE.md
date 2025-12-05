# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates a comprehensive HTML maintenance guide for the Melitta Caffeo Solo & Milk coffee machine. The main artifact is a single self-contained HTML file with inline CSS and base64-encoded images, containing brief steps for all maintenance procedures with icons and visual indicators.

## Technology Stack

- Python 3.12
- uv (project manager)
- Output: Single HTML file with inline CSS and inline base64 images

## Build Commands

```bash
# Initialize project (if not done)
uv init

# Install dependencies
uv sync

# Run the main script to generate HTML
uv run python main.py
```

## Source Material

The `MelittaCaffeoSoloAndMilkManual.pdf` contains the official operating instructions. Key maintenance procedures to document:

### Daily Maintenance
- Empty drip tray
- Empty coffee grounds container
- Wipe exterior with damp cloth

### Regular Maintenance
- **Steam pipe cleaning**: After each use, rinse with water; periodically disassemble and clean nozzle
- **Brewing unit cleaning**: Weekly - remove, rinse with water, let dry
- **Water filter replacement**: Every 2 months or when filter indicator lights up

### Periodic Maintenance (with integrated programs)
- **Cleaning program** (~15 min): Every 2 months or after 200 cups - uses Melitta cleaning tabs
- **Descaling program** (~30 min): Every 3 months or when descale indicator lights up - uses Melitta ANTI CALC

### Machine Component Reference
- Component 1: Drip tray with cup plate and coffee grounds container
- Component 7: Water reservoir
- Component 11: Valve switch for steam/hot water
- Component 12: Steam pipe
- Component 13: Right cover (access to brewing unit and grinder adjustment)

## HTML Output Requirements

- Self-contained single HTML file
- Inline CSS (no external stylesheets)
- Images encoded as base64 data URIs
- Icons and visual indicators for each procedure
- Brief, step-by-step instructions
- Mobile-friendly responsive design
