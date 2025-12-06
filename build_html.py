#!/usr/bin/env python3
"""Build HTML maintenance guide with inline CSS and base64 images."""

import base64
import os

from weasyprint import HTML

ICONS_DIR = "assets/icons"
OUTPUT_FILE = "melitta_caffeo_solo_milk_maintenance_guide.html"
PDF_FILE = "melitta_caffeo_solo_milk_maintenance_guide.pdf"


def img_to_base64(filepath):
    """Convert image file to base64 data URI."""
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"


def load_images():
    """Load all icons as base64."""
    images = {}
    for filename in os.listdir(ICONS_DIR):
        if filename.endswith(".png"):
            name = filename[:-4]  # Remove .png
            images[name] = img_to_base64(os.path.join(ICONS_DIR, filename))
    return images


def build_html(images):
    """Build the complete HTML file."""

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Melitta Caffeo Solo & Milk - Maintenance Guide</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.5;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #1a1a1a 0%, #333 100%);
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
        }}

        header h1 {{
            font-size: 1.8em;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        header p {{
            opacity: 0.8;
            font-size: 0.95em;
        }}

        .section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .section h2 {{
            font-size: 1.3em;
            color: #1a1a1a;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e74c3c;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section h2 img {{
            height: 32px;
            width: auto;
        }}

        .section h3 {{
            font-size: 1.1em;
            color: #1a1a1a;
            margin: 25px 0 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e74c3c;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .frequency {{
            display: inline-block;
            background: #e74c3c;
            color: white;
            font-size: 0.7em;
            padding: 3px 10px;
            border-radius: 20px;
            font-weight: 500;
            margin-left: auto;
        }}

        .frequency.daily {{ background: #27ae60; }}
        .frequency.weekly {{ background: #3498db; }}
        .frequency.monthly {{ background: #9b59b6; }}
        .frequency.asneeded {{ background: #e67e22; }}

        .duration {{
            display: inline-block;
            background: #555;
            color: white;
            font-size: 0.7em;
            padding: 3px 10px;
            border-radius: 20px;
            font-weight: 500;
            margin-left: 8px;
        }}

        .time {{
            display: inline-block;
            background: #666;
            color: white;
            font-size: 0.85em;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 500;
            white-space: nowrap;
        }}

        .steps {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .step {{
            display: flex;
            align-items: flex-start;
            gap: 15px;
            padding: 15px;
            background: #fafafa;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
        }}

        .step-number {{
            background: #e74c3c;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.85em;
            flex-shrink: 0;
        }}

        .step-content {{
            flex: 1;
        }}

        .step-content p {{
            margin: 0;
        }}

        .step img.diagram {{
            max-width: 280px;
            height: auto;
            border-radius: 8px;
            margin-top: 10px;
            border: 1px solid #eee;
            object-fit: contain;
        }}

        img {{
            max-width: 100%;
            height: auto;
            object-fit: contain;
        }}

        .indicator-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(3, auto);
            grid-auto-flow: column;
            gap: 15px;
            margin-top: 15px;
        }}

        .indicator {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 15px;
            background: #fafafa;
            border-radius: 8px;
        }}

        a.indicator {{
            text-decoration: none;
            color: inherit;
            transition: background 0.2s, transform 0.2s;
        }}

        a.indicator:hover {{
            background: #f0f0f0;
            transform: translateY(-2px);
        }}

        .indicator img {{
            height: 36px;
            width: auto;
        }}

        .indicator-text {{
            font-size: 0.9em;
        }}

        .indicator-text strong {{
            display: block;
            color: #1a1a1a;
        }}

        .indicator-text span {{
            color: #666;
            font-size: 0.85em;
        }}

        .button-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 8px 0;
        }}

        .button-row img {{
            height: 24px;
            width: auto;
        }}

        .supplies {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 12px 15px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}

        .supplies strong {{
            color: #856404;
        }}

        .warning {{
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 12px 15px;
            margin: 15px 0;
            font-size: 0.9em;
            color: #721c24;
        }}

        .tip {{
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 8px;
            padding: 12px 15px;
            margin: 15px 0;
            font-size: 0.9em;
            color: #0c5460;
        }}

        .diagram-row {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 15px 0;
            align-items: flex-start;
        }}

        .diagram-row img {{
            height: 180px;
            width: auto;
            border-radius: 8px;
            border: 1px solid #eee;
            object-fit: contain;
        }}

        img.diagram {{
            height: 180px;
            width: auto;
            object-fit: contain;
        }}

        .machine-overview {{
            text-align: center;
            margin: 20px 0;
        }}

        .machine-overview img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 10px;
                font-size: 14px;
            }}

            header h1 {{
                font-size: 1.4em;
            }}

            .section {{
                padding: 15px;
            }}

            .section h2 {{
                flex-wrap: wrap;
                font-size: 1.1em;
            }}

            .indicator-grid {{
                grid-template-columns: 1fr;
                grid-auto-flow: row;
            }}

            .button-row {{
                flex-wrap: wrap;
                justify-content: center;
            }}

            .step {{
                flex-direction: column;
            }}

            .diagram-row {{
                flex-direction: column;
                align-items: center;
            }}

            .diagram-row img {{
                max-width: 100%;
                height: auto;
                max-height: 180px;
            }}
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
                max-width: none;
            }}

            header {{
                background: none;
                color: #1a1a1a;
                border: 2px solid #333;
                padding: 15px 20px;
            }}

            header p {{
                opacity: 1;
            }}

            .section {{
                break-inside: avoid;
                page-break-inside: avoid;
                margin-bottom: 40px;
                box-shadow: none;
                border: 1px solid #ccc;
                padding: 20px;
            }}

            .section h2 {{
                border-bottom-color: #333;
            }}

            .section h3 {{
                border-bottom-color: #333;
            }}

            .frequency, .duration, .time {{
                background: none;
                color: #333;
                border: 1px solid #333;
            }}

            .step {{
                background: none;
                border-left: 2px solid #333;
                padding: 10px 15px;
            }}

            .step-number {{
                background: none;
                color: #333;
                border: 2px solid #333;
            }}

            .indicator {{
                background: none;
                border: 1px solid #ddd;
            }}

            .steps {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}

            .step {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}

            .indicator-grid {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}

            .diagram-row {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}

            h2 {{
                break-after: avoid;
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Melitta Caffeo Solo & Milk</h1>
        <p>Maintenance Guide</p>
    </header>

    <!-- Display Indicators Reference -->
    <div class="section">
        <h2>Display Indicators</h2>
        <div class="indicator-grid">
            <div class="indicator">
                <img src="{images['icon_power']}" alt="Power">
                <div class="indicator-text">
                    <strong>Power</strong>
                    <span>Ready / Heating</span>
                </div>
            </div>
            <a href="#daily" class="indicator">
                <img src="{images['icon_beans']}" alt="Beans">
                <div class="indicator-text">
                    <strong>Beans</strong>
                    <span>Refill beans &rarr;</span>
                </div>
            </a>
            <a href="#daily" class="indicator">
                <img src="{images['icon_water']}" alt="Water">
                <div class="indicator-text">
                    <strong>Water</strong>
                    <span>Fill reservoir &rarr;</span>
                </div>
            </a>
            <a href="#daily" class="indicator">
                <img src="{images['icon_drip_tray']}" alt="Drip Tray">
                <div class="indicator-text">
                    <strong>Drip Tray</strong>
                    <span>Empty required &rarr;</span>
                </div>
            </a>
            <a href="#steam" class="indicator">
                <img src="{images['icon_steam']}" alt="Steam">
                <div class="indicator-text">
                    <strong>Steam</strong>
                    <span>Steam pipe &rarr;</span>
                </div>
            </a>
            <a href="#filter" class="indicator">
                <img src="{images['icon_filter']}" alt="Filter">
                <div class="indicator-text">
                    <strong>Filter</strong>
                    <span>Replace filter &rarr;</span>
                </div>
            </a>
            <a href="#cleaning" class="indicator">
                <img src="{images['icon_clean']}" alt="Clean">
                <div class="indicator-text">
                    <strong>Clean</strong>
                    <span>Run cleaning &rarr;</span>
                </div>
            </a>
            <a href="#descaling" class="indicator">
                <img src="{images['icon_descale']}" alt="Descale">
                <div class="indicator-text">
                    <strong>Descale</strong>
                    <span>Run descaling &rarr;</span>
                </div>
            </a>
        </div>
    </div>

    <!-- Daily Maintenance -->
    <div class="section" id="daily">
        <h2>
            <img src="{images['icon_drip_tray']}" alt="">
            Daily Maintenance
            <span class="frequency daily">Daily</span>
        </h2>
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p><strong>Empty drip tray</strong> and coffee grounds container</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p><strong>Refill beans</strong> if low</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p><strong>Fill water reservoir</strong> with fresh water</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <p><strong>Wipe exterior</strong> with soft damp cloth</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Steam Pipe Cleaning -->
    <div class="section" id="steam">
        <h2>
            <img src="{images['icon_steam']}" alt="">
            Steam Pipe Cleaning
            <span class="frequency daily">After Each Use</span>
        </h2>
        <div class="tip">Rinse the steam pipe after every use to prevent milk residue buildup.</div>
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p>Fill vessel with clear water, immerse steam pipe tip</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p>Press <img src="{images['btn_steam']}" alt="steam" style="height:20px;vertical-align:middle"> button, wait for <img src="{images['icon_steam']}" alt="" style="height:20px;vertical-align:middle"> to illuminate</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p>Turn valve clockwise <span class="time">🕐 5 sec</span>, close, wait <span class="time">🕐 30 sec</span></p>
                </div>
            </div>
        </div>

        <h3 style="margin: 25px 0 15px; font-size: 1.1em;">Deep Clean (Weekly)</h3>
        <div class="diagram-row">
            <img src="{images['diagram_steam_pipe_twist']}" alt="Twist off steam pipe">
            <img src="{images['diagram_steam_pipe_parts']}" alt="Steam pipe parts">
            <img src="{images['diagram_nozzle_clean']}" alt="Clean nozzle">
        </div>
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p><strong>Twist off</strong> steam pipe (turn in arrow direction)</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p><strong>Pull nozzle</strong> out of steam pipe</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p><strong>Clean nozzle</strong> with pointed object or brush</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <p><strong>Rinse all parts</strong> with water, reassemble</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Brewing Unit Cleaning -->
    <div class="section" id="brewing">
        <h2>
            Brewing Unit Cleaning
            <span class="frequency weekly">Weekly</span>
        </h2>
        <div class="warning">Switch off appliance and unplug before cleaning!</div>
        <div class="diagram-row">
            <img src="{images['diagram_brewing_unit_remove']}" alt="Remove brewing unit">
            <img src="{images['diagram_brewing_chamber']}" alt="Brewing chamber">
        </div>
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p><strong>Remove cover</strong> (pull right side panel off)</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p><strong>Press red button</strong> on handle, turn clockwise, pull out</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p><strong>Rinse thoroughly</strong> with clear water on all sides</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <p><strong>Let dry</strong>, remove coffee residues from machine</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <p><strong>Reinsert</strong> brewing unit, turn counterclockwise until locked</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Cleaning Program -->
    <div class="section" id="cleaning">
        <h2>
            <img src="{images['icon_clean']}" alt="">
            Cleaning Program
            <span class="frequency monthly">Every 2 months / 200 cups</span>
            <span class="duration">🕐 ~15 min</span>
        </h2>
        <div class="supplies"><strong>Required:</strong> Melitta Cleaning Tabs</div>
        <div class="tip">Do not interrupt the program.</div>

        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p><strong>Switch off</strong>, fill water reservoir to MAX</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p>Hold <img src="{images['btn_coffee']}" alt="coffee" style="height:18px;vertical-align:middle"> + <img src="{images['btn_power']}" alt="power" style="height:18px;vertical-align:middle"> for 2 sec &rarr; <img src="{images['icon_clean']}" alt="" style="height:20px;vertical-align:middle"> flashes</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p><strong>Empty drip tray</strong>, reinsert without grounds container</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <p>When <img src="{images['btn_power']}" alt="" style="height:18px;vertical-align:middle"> lights: <strong>remove brewing unit</strong>, insert cleaning tab, reinstall</p>
                    <img src="{images['diagram_brewing_unit_clean_tab']}" alt="Insert cleaning tab" class="diagram">
                </div>
            </div>
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <p><strong>Refill water</strong> to MAX, press <img src="{images['btn_steam']}" alt="steam" style="height:18px;vertical-align:middle"> to continue <span class="time">🕐 ~5 min</span></p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">6</div>
                <div class="step-content">
                    <p>When complete: <strong>empty and reinsert</strong> drip tray + grounds container</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Descaling Program -->
    <div class="section" id="descaling">
        <h2>
            <img src="{images['icon_descale']}" alt="">
            Descaling Program
            <span class="frequency monthly">Every 3 months</span>
            <span class="duration">🕐 ~30 min</span>
        </h2>
        <div class="supplies"><strong>Required:</strong> Melitta ANTI CALC descaler</div>
        <div class="warning">Descaling agent can cause skin irritation. Follow safety instructions on packaging.</div>

        <img src="{images['diagram_descale_setup']}" alt="Descaling setup" style="height:180px;width:auto;border-radius:8px;margin:15px 0;border:1px solid #eee">

        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p><strong>Attach hose</strong> to steam pipe, place in grounds container</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p><strong>Remove water filter</strong> if installed</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p>Hold <img src="{images['btn_steam']}" alt="steam" style="height:18px;vertical-align:middle"> + <img src="{images['btn_power']}" alt="power" style="height:18px;vertical-align:middle"> for 3 sec &rarr; <img src="{images['icon_descale']}" alt="" style="height:20px;vertical-align:middle"> flashes</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <p><strong>Empty and reinsert</strong> drip tray</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <p><strong>Empty water reservoir</strong>, add 100ml descaler + fill to MAX (Melitta ANTI CALC)</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">6</div>
                <div class="step-content">
                    <p>Press <img src="{images['btn_steam']}" alt="steam" style="height:18px;vertical-align:middle"> to start <span class="time">🕐 ~15 min</span></p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">7</div>
                <div class="step-content">
                    <p>When <img src="{images['icon_steam']}" alt="" style="height:20px;vertical-align:middle"> lights: <strong>turn valve clockwise</strong> until stop <span class="time">🕐 ~10 min</span></p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">8</div>
                <div class="step-content">
                    <p><strong>Empty all containers</strong>, rinse reservoir, fill with fresh water</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">9</div>
                <div class="step-content">
                    <p>Press <img src="{images['btn_steam']}" alt="steam" style="height:18px;vertical-align:middle"> for final rinse, <strong>close valve</strong> when <img src="{images['icon_steam']}" alt="" style="height:20px;vertical-align:middle"> lights</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">10</div>
                <div class="step-content">
                    <p>When <img src="{images['btn_power']}" alt="" style="height:18px;vertical-align:middle"> lights: <strong>done!</strong> Reinstall water filter if used</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Water Filter -->
    <div class="section" id="filter">
        <h2>
            <img src="{images['icon_filter']}" alt="">
            Water Filter Replacement
            <span class="frequency monthly">Every 2 months</span>
        </h2>
        <div class="supplies"><strong>Required:</strong> Melitta Claris Water Filter</div>
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p><strong>Soak new filter</strong> in glass of water for several minutes</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p><strong>Switch off</strong>, hold <img src="{images['btn_strength']}" alt="strength" style="height:18px;vertical-align:middle"> + <img src="{images['btn_power']}" alt="power" style="height:18px;vertical-align:middle"> for 3 sec</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p><strong>Empty drip tray</strong>, reinsert without grounds container</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <p><strong>Remove & empty</strong> water reservoir, screw filter onto thread at bottom</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <p><strong>Fill reservoir</strong> to MAX, reinsert</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">6</div>
                <div class="step-content">
                    <p><strong>Place container</strong> under steam pipe, turn valve clockwise until water flows</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">7</div>
                <div class="step-content">
                    <p>When <img src="{images['icon_steam']}" alt="" style="height:20px;vertical-align:middle"> lights: <strong>close valve</strong> &rarr; Ready!</p>
                </div>
            </div>
        </div>
        <div class="tip">Water may be cloudy during first rinse (activated carbon). This is normal.</div>
    </div>

    <!-- Steam Pipe Positions -->
    <div class="section">
        <h2>
            <img src="{images['icon_steam']}" alt="">
            Steam Pipe Positions
        </h2>
        <img src="{images['diagram_steam_positions']}" alt="Steam pipe positions" style="height:180px;width:auto;border-radius:8px;margin:15px 0;border:1px solid #eee">
        <div class="indicator-grid">
            <div class="indicator">
                <strong style="font-size:1.5em;margin-right:10px">&darr;</strong>
                <div class="indicator-text">
                    <strong>Position 1 (Down)</strong>
                    <span>For frothing milk</span>
                </div>
            </div>
            <div class="indicator">
                <strong style="font-size:1.5em;margin-right:10px">&uarr;</strong>
                <div class="indicator-text">
                    <strong>Position 2 (Up)</strong>
                    <span>For heating milk / hot water</span>
                </div>
            </div>
        </div>
    </div>

    <footer style="text-align:center;padding:30px;color:#666;font-size:0.85em;">
        Based on Melitta Caffeo Solo & Milk Operating Instructions<br>
        For complete instructions, refer to the original manual
    </footer>
</body>
</html>'''

    return html


def main():
    print("Loading images...")
    images = load_images()
    print(f"Loaded {len(images)} images")

    print("Building HTML...")
    html = build_html(images)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    file_size = os.path.getsize(OUTPUT_FILE)
    print(f"\nCreated: {OUTPUT_FILE}")
    print(f"Size: {file_size / 1024:.1f} KB")

    print("Generating PDF...")
    # Remove clock emoji for PDF (emoji doesn't render in WeasyPrint)
    pdf_html = html.replace("🕐 ", "")
    HTML(string=pdf_html).write_pdf(PDF_FILE)
    pdf_size = os.path.getsize(PDF_FILE)
    print(f"Created: {PDF_FILE}")
    print(f"Size: {pdf_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
