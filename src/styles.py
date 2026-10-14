"""UI Design System, Color Tokens, and Styling Helpers for EcoRoute."""

import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# =====================================================================
# WCAG AA COMPLIANT COLOR DESIGN SYSTEM
# =====================================================================
# Light Surface Tokens
COLOR_BG = "#F7F9F6"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY_GREEN = "#176B45"      # High contrast green
COLOR_FOREST_GREEN = "#103D2B"       # Deep green for headings
COLOR_LIGHT_GREEN = "#E8F4EC"        # Subtle surface tint
COLOR_TEXT_MAIN = "#17231C"          # Primary dark text
COLOR_TEXT_SECONDARY = "#526158"     # Secondary body/subtitles
COLOR_TEXT_MUTED = "#65736A"         # Muted captions & labels
COLOR_BORDER = "#D8E2DA"             # Crisp border
COLOR_INPUT_BORDER = "#CBD7CE"       # Input field border
COLOR_BUTTON_HOVER = "#105437"       # Primary button hover

# Dark Green Card Tokens
COLOR_DARK_TEXT_MAIN = "#FFFFFF"
COLOR_DARK_TEXT_SEC = "#E3F4E9"
COLOR_DARK_METRIC_LABEL = "#C5E8D3"
COLOR_DARK_MUTED = "#A7D8BE"

# Status & Alert Tokens
COLOR_AMBER = "#B45309"              # Accessible amber (>4.5:1 on light)
COLOR_AMBER_BG = "#FFFBEB"
COLOR_AMBER_BORDER = "#FDE68A"
COLOR_RED = "#B91C1C"                # Accessible red
COLOR_RED_BG = "#FEF2F2"
COLOR_RED_BORDER = "#FECACA"

# Geographic coordinates for Kochi - Thrissur road network corridor
WAYPOINT_COORDS = {
    "Kochi": [76.3073, 9.9982],
    "Aluva": [76.3570, 10.1076],
    "Angamaly": [76.3860, 10.1960],
    "Chalakudy": [76.3330, 10.3070],
    "Ollur": [76.2410, 10.4720],
    "Thrissur": [76.2144, 10.5276],
    "Kalady": [76.4320, 10.1680],
    "Ezhattumugham": [76.4710, 10.2310],
    "Pudukkad": [76.2620, 10.4180],
    "Perumbavoor": [76.4800, 10.1115],
    "Mala": [76.2995, 10.2285],
    "Kodungallur": [76.1971, 10.2277],
    "Irinjalakuda": [76.2050, 10.3420],
}

ROUTE_PATHS = {
    "R1": [
        WAYPOINT_COORDS["Kochi"],
        WAYPOINT_COORDS["Aluva"],
        WAYPOINT_COORDS["Angamaly"],
        WAYPOINT_COORDS["Chalakudy"],
        WAYPOINT_COORDS["Ollur"],
        WAYPOINT_COORDS["Thrissur"],
    ],
    "R2": [
        WAYPOINT_COORDS["Kochi"],
        WAYPOINT_COORDS["Aluva"],
        WAYPOINT_COORDS["Kalady"],
        WAYPOINT_COORDS["Ezhattumugham"],
        WAYPOINT_COORDS["Chalakudy"],
        WAYPOINT_COORDS["Pudukkad"],
        WAYPOINT_COORDS["Thrissur"],
    ],
    "R3": [
        WAYPOINT_COORDS["Kochi"],
        WAYPOINT_COORDS["Perumbavoor"],
        WAYPOINT_COORDS["Mala"],
        WAYPOINT_COORDS["Kodungallur"],
        WAYPOINT_COORDS["Irinjalakuda"],
        WAYPOINT_COORDS["Thrissur"],
    ],
}


def inject_custom_css():
    """
    Inject high-contrast CSS styling ensuring WCAG AA readability
    for light surfaces, widgets, inputs, and dark-green cards.
    """
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400..700&family=Space+Grotesk:wght@500;600;700&display=swap');

        /* Base Variables */
        :root {{
            --bg-main: {COLOR_BG};
            --card-bg: {COLOR_CARD};
            --primary-green: {COLOR_PRIMARY_GREEN};
            --forest-green: {COLOR_FOREST_GREEN};
            --light-green: {COLOR_LIGHT_GREEN};
            --text-main: {COLOR_TEXT_MAIN};
            --text-sec: {COLOR_TEXT_SECONDARY};
            --text-muted: {COLOR_TEXT_MUTED};
            --border-color: {COLOR_BORDER};
            --input-border: {COLOR_INPUT_BORDER};
            --btn-hover: {COLOR_BUTTON_HOVER};
        }}

        /* App & Global Typography */
        [data-testid="stAppViewContainer"] {{
            background-color: var(--bg-main) !important;
            color: var(--text-main) !important;
        }}

        [data-testid="stHeader"] {{
            background-color: rgba(247, 249, 246, 0.92) !important;
            backdrop-filter: blur(8px);
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: var(--forest-green) !important;
            letter-spacing: -0.015em !important;
        }}

        h1 {{
            font-size: clamp(1.8rem, 3.2vw, 2.5rem) !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            margin-bottom: 0.35rem !important;
        }}

        h2 {{
            font-size: 1.45rem !important;
            font-weight: 600 !important;
            margin-top: 0.75rem !important;
            margin-bottom: 0.5rem !important;
        }}

        h3 {{
            font-size: 1.15rem !important;
            font-weight: 600 !important;
        }}

        p, span, div, label, li {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-main);
        }}

        /* Sidebar Styling & High-Contrast Navigation */
        [data-testid="stSidebar"] {{
            background-color: #FFFFFF !important;
            border-right: 1px solid var(--border-color) !important;
        }}

        [data-testid="stSidebar"] * {{
            color: var(--text-main);
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] > label {{
            display: none !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] > div {{
            gap: 4px !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label {{
            background-color: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 8px !important;
            padding: 8px 12px !important;
            margin-bottom: 2px !important;
            cursor: pointer !important;
            transition: all 0.15s ease-in-out !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label p,
        [data-testid="stSidebar"] [data-testid="stRadio"] label span {{
            color: var(--text-main) !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
            background-color: var(--light-green) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover p,
        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover span {{
            color: var(--primary-green) !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
            background-color: var(--light-green) !important;
            border: 1px solid #C8DFD0 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,
        [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {{
            color: var(--primary-green) !important;
            font-weight: 700 !important;
        }}

        /* Radio Selection Dot */
        [data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div {{
            border-color: var(--primary-green) !important;
            background-color: var(--primary-green) !important;
        }}

        /* Sidebar Expander & Sliders */
        details[data-testid="stExpander"] {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 4px rgba(16, 61, 43, 0.03) !important;
        }}

        details[data-testid="stExpander"] summary {{
            color: var(--forest-green) !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 10px 14px !important;
        }}

        details[data-testid="stExpander"] summary svg {{
            fill: var(--forest-green) !important;
            stroke: var(--forest-green) !important;
        }}

        details[data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
            padding: 12px 14px !important;
        }}

        div[data-testid="stSlider"] label p {{
            color: var(--text-main) !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
        }}

        div[data-testid="stSlider"] [data-testid="stThumbValue"] {{
            color: var(--forest-green) !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stSlider"] [data-testid="stTickBarMin"],
        div[data-testid="stSlider"] [data-testid="stTickBarMax"] {{
            color: var(--text-muted) !important;
            font-size: 0.75rem !important;
        }}

        /* Input Fields: High-Contrast & Clear Borders */
        div[data-testid="stWidgetLabel"] label p {{
            color: var(--text-main) !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            margin-bottom: 4px !important;
        }}

        div[data-baseweb="input"] {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--input-border) !important;
            border-radius: 8px !important;
            transition: border-color 0.15s ease !important;
        }}

        div[data-baseweb="input"]:focus-within {{
            border-color: var(--primary-green) !important;
            box-shadow: 0 0 0 2px rgba(23, 107, 69, 0.15) !important;
        }}

        div[data-baseweb="input"] input {{
            color: var(--text-main) !important;
            -webkit-text-fill-color: var(--text-main) !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            background-color: transparent !important;
        }}

        div[data-baseweb="input"] input::placeholder {{
            color: var(--text-muted) !important;
            opacity: 1 !important;
        }}

        div[data-baseweb="select"] > div {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--input-border) !important;
            border-radius: 8px !important;
            color: var(--text-main) !important;
        }}

        div[data-baseweb="select"] span {{
            color: var(--text-main) !important;
            font-weight: 500 !important;
            font-size: 0.92rem !important;
        }}

        div[data-baseweb="popover"] {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            box-shadow: 0 6px 20px rgba(16, 61, 43, 0.08) !important;
        }}

        div[data-baseweb="popover"] li {{
            color: var(--text-main) !important;
            font-size: 0.9rem !important;
        }}

        div[data-baseweb="popover"] li:hover {{
            background-color: var(--light-green) !important;
            color: var(--primary-green) !important;
        }}

        /* Buttons: High Contrast Action States */
        .stButton > button[kind="primary"] {{
            background-color: var(--primary-green) !important;
            color: #FFFFFF !important;
            border: 1px solid var(--primary-green) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 9px 18px !important;
            box-shadow: 0 2px 8px rgba(23, 107, 69, 0.2) !important;
            transition: all 0.15s ease !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background-color: var(--btn-hover) !important;
            border-color: var(--btn-hover) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(16, 61, 43, 0.3) !important;
        }}

        .stButton > button:not([kind="primary"]) {{
            background-color: #FFFFFF !important;
            color: var(--text-main) !important;
            border: 1px solid var(--input-border) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            transition: all 0.15s ease !important;
        }}

        .stButton > button:not([kind="primary"]):hover {{
            background-color: var(--light-green) !important;
            color: var(--primary-green) !important;
            border-color: #C8DFD0 !important;
        }}

        /* Cards & Hero */
        .eco-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 20px 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 12px rgba(16, 61, 43, 0.03);
        }}

        .eco-hero {{
            background: linear-gradient(135deg, var(--light-green) 0%, #FFFFFF 100%);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 26px 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 18px rgba(23, 107, 69, 0.04);
        }}

        .eco-hero h1 {{
            color: var(--forest-green) !important;
            margin: 4px 0 6px 0 !important;
        }}

        .eco-eyebrow {{
            color: var(--primary-green) !important;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .eco-subtitle {{
            color: var(--text-sec) !important;
            font-size: 0.98rem;
            line-height: 1.5;
            margin: 0;
            font-weight: 400;
        }}

        /* KPI Metric Cards */
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 14px;
            margin-bottom: 20px;
        }}

        .kpi-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px 18px;
            box-shadow: 0 2px 8px rgba(16, 61, 43, 0.03);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .kpi-label {{
            color: var(--text-sec) !important;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .kpi-value {{
            color: var(--forest-green) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.65rem;
            font-weight: 700;
            line-height: 1.2;
        }}

        .kpi-delta {{
            font-size: 0.78rem;
            font-weight: 600;
            margin-top: 4px;
            color: var(--primary-green) !important;
        }}

        /* Built-in Streamlit Metrics */
        [data-testid="stMetric"] {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            box-shadow: 0 2px 8px rgba(16, 61, 43, 0.03) !important;
        }}

        [data-testid="stMetricLabel"] p {{
            color: var(--text-sec) !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
        }}

        [data-testid="stMetricValue"] div {{
            color: var(--forest-green) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.65rem !important;
            font-weight: 700 !important;
        }}

        /* Dark-Green Recommendation Banner (Explicit Light Elements on Dark) */
        .rec-banner {{
            background: linear-gradient(130deg, var(--forest-green) 0%, #174E38 100%) !important;
            border-radius: 14px;
            padding: 22px 26px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px rgba(16, 61, 43, 0.16);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .rec-banner * {{
            color: #FFFFFF;
        }}

        .rec-tag {{
            background-color: rgba(255, 255, 255, 0.18) !important;
            color: #E3F4E9 !important;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            width: fit-content;
        }}

        .rec-title {{
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            margin: 0 !important;
        }}

        .rec-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin-top: 6px;
            border-top: 1px solid rgba(255, 255, 255, 0.18);
            padding-top: 14px;
        }}

        .rec-item-label {{
            font-size: 0.74rem !important;
            color: #C5E8D3 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            font-weight: 600 !important;
            margin-bottom: 2px !important;
        }}

        .rec-item-val {{
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
        }}

        /* Status Pills */
        .pill {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        .pill-green {{
            background-color: var(--light-green);
            color: var(--forest-green);
            border: 1px solid #C4E2CF;
        }}

        .pill-amber {{
            background-color: {COLOR_AMBER_BG};
            color: {COLOR_AMBER};
            border: 1px solid {COLOR_AMBER_BORDER};
        }}

        .pill-red {{
            background-color: {COLOR_RED_BG};
            color: {COLOR_RED};
            border: 1px solid {COLOR_RED_BORDER};
        }}

        .pill-neutral {{
            background-color: #F1F4F2;
            color: var(--text-sec);
            border: 1px solid var(--border-color);
        }}

        /* Callout / Disclosures */
        .demo-callout {{
            background-color: {COLOR_AMBER_BG};
            border: 1px solid {COLOR_AMBER_BORDER};
            border-left: 4px solid {COLOR_AMBER};
            border-radius: 8px;
            padding: 10px 14px;
            color: #78350F;
            font-size: 0.85rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            line-height: 1.45;
        }}

        .demo-callout strong {{
            color: #92400E;
        }}

        /* Tabs */
        [data-testid="stTabs"] button {{
            color: var(--text-sec) !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            border-bottom: 2px solid transparent !important;
            padding: 8px 16px !important;
        }}

        [data-testid="stTabs"] button[aria-selected="true"] {{
            color: var(--primary-green) !important;
            border-bottom-color: var(--primary-green) !important;
            font-weight: 700 !important;
        }}

        /* Tables & Dataframes */
        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border-color) !important;
            border-radius: 10px !important;
            overflow: hidden !important;
        }}

        /* Map Legend */
        .map-legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px 14px;
            margin-top: 10px;
            font-size: 0.82rem;
            align-items: center;
            color: var(--text-main);
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-sec);
        }}

        .legend-bullet {{
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(eyebrow: str, title: str, subtitle: str):
    """Render a clean, responsive hero header with accessible high-contrast text."""
    st.markdown(
        f"""
        <div class="eco-hero">
            <div class="eco-eyebrow">🌱 {eyebrow}</div>
            <h1>{title}</h1>
            <p class="eco-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_demo_badge():
    """Render an honest, accessible transparency badge."""
    st.markdown(
        """
        <div class="demo-callout">
            <span style="font-size: 1.1rem;">⚠️</span>
            <div>
                <strong>BENCHMARK & ESTIMATION DATA:</strong> Routes, traffic metrics, and fuel values reflect calibrated project benchmarks and standard vehicle emission coefficients, not live telemetry.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_route_map(routes_df, recommended_route_id="R1"):
    """
    Generate an interactive Pydeck Map displaying real Kerala road network corridors.
    Renders actual paths, origin/destination markers, and bounding viewpoints.
    """
    path_data = []

    for _, row in routes_df.iterrows():
        rid = row["route_id"]
        coords = ROUTE_PATHS.get(rid)
        if not coords:
            continue

        is_recommended = (rid == recommended_route_id)
        if is_recommended:
            color = [23, 107, 69, 245]   # Primary green
            width = 6
        elif rid == "R2":
            color = [180, 83, 9, 230]    # Accessible amber
            width = 4
        else:
            color = [101, 115, 106, 200] # High contrast muted gray-green
            width = 3

        path_data.append({
            "route_id": rid,
            "route_name": row["route_name"],
            "path": coords,
            "color": color,
            "width": width,
            "distance_km": row["distance_km"],
            "travel_time_min": row["travel_time_min"],
        })

    points_data = [
        {"name": "Kochi (Origin)", "coords": WAYPOINT_COORDS["Kochi"], "color": [16, 61, 43], "radius": 280},
        {"name": "Aluva (Junction)", "coords": WAYPOINT_COORDS["Aluva"], "color": [82, 97, 88], "radius": 160},
        {"name": "Angamaly", "coords": WAYPOINT_COORDS["Angamaly"], "color": [82, 97, 88], "radius": 160},
        {"name": "Chalakudy", "coords": WAYPOINT_COORDS["Chalakudy"], "color": [82, 97, 88], "radius": 160},
        {"name": "Kodungallur", "coords": WAYPOINT_COORDS["Kodungallur"], "color": [82, 97, 88], "radius": 160},
        {"name": "Thrissur (Destination)", "coords": WAYPOINT_COORDS["Thrissur"], "color": [180, 83, 9], "radius": 280},
    ]

    path_layer = pdk.Layer(
        "PathLayer",
        data=path_data,
        get_path="path",
        get_color="color",
        get_width="width",
        width_scale=20,
        width_min_pixels=3,
        pickable=True,
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=points_data,
        get_position="coords",
        get_color="color",
        get_radius="radius",
        radius_min_pixels=5,
        radius_max_pixels=12,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=10.26,
        longitude=76.33,
        zoom=9.3,
        pitch=25,
        bearing=0,
    )

    deck = pdk.Deck(
        layers=[path_layer, scatter_layer],
        initial_view_state=view_state,
        map_provider="carto",
        map_style="light",
        tooltip={
            "html": "<b style='color:#FFFFFF'>{name}</b><br><span style='color:#C5E8D3'>{route_name}</span><br>Distance: {distance_km} km | Time: {travel_time_min} min",
            "style": {"backgroundColor": "#103D2B", "color": "#FFFFFF", "fontSize": "12px", "borderRadius": "6px", "padding": "8px"},
        },
    )
    return deck


def get_plotly_theme():
    """Return consistent, high-contrast styling dict for Plotly charts."""
    return {
        "layout": {
            "paper_bgcolor": "#FFFFFF",
            "plot_bgcolor": "#FFFFFF",
            "font": {"family": "DM Sans, sans-serif", "color": COLOR_TEXT_MAIN, "size": 12},
            "margin": {"l": 45, "r": 20, "t": 35, "b": 35},
            "xaxis": {"gridcolor": "#EEF3EF", "zerolinecolor": "#D8E2DA", "tickfont": {"color": COLOR_TEXT_SECONDARY}},
            "yaxis": {"gridcolor": "#EEF3EF", "zerolinecolor": "#D8E2DA", "tickfont": {"color": COLOR_TEXT_SECONDARY}},
        }
    }
