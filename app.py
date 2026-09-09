"""EcoRoute: a transparent, sample-data route optimization demo."""

from pathlib import Path
import pandas as pd
import streamlit as st

from src.route import enrich_routes, route_recommendations
PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"

st.set_page_config(
    page_title="EcoRoute | Smarter journeys, lighter impact",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --ink:#153332; --muted:#637472; --mint:#dff3e9; --green:#16845b; --orange:#e9874d; --line:#dce8e3; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    [data-testid="stAppViewContainer"] { background: #f7faf8; }
    [data-testid="stHeader"] { background: transparent; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
    h1 { font-size: clamp(2.1rem, 5vw, 4.2rem); line-height: 1.02; }
    [data-testid="stMetric"] { background: white; border: 1px solid var(--line); border-radius: 8px; padding: 15px; }
    .hero { background: linear-gradient(120deg, #dff3e9 0%, #f7faf8 68%); border: 1px solid #cbe6d9; border-radius: 10px; padding: 28px 34px; margin-bottom: 22px; }
    .eyebrow { color: var(--green); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: .78rem; }
    .demo-note { color: #71502d; background: #fff1dc; border-left: 4px solid var(--orange); padding: 10px 13px; border-radius: 4px; font-size: .9rem; }
    .route-banner { background: var(--ink); color: white; border-radius: 8px; padding: 18px 20px; }
    .route-banner small { color: #acd8c4; text-transform: uppercase; letter-spacing: .08em; }
    .route-banner strong { display:block; font-size: 1.3rem; margin-top: 3px; }
    .section-label { color: var(--muted); text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; font-weight: 700; margin: 22px 0 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)
@st.cache_data
def load_data():
    return (
        pd.read_csv(DATA_DIR / "vehicles.csv"),
        pd.read_csv(DATA_DIR / "routes.csv"),
    )
vehicles, routes = load_data()

st.markdown(
    '<div class="hero"><div class="eyebrow">Route intelligence for everyday travel</div>'
    '<h1>Go farther.<br>Leave less behind.</h1>'
    '<p>EcoRoute compares realistic route trade-offs so you can choose a journey that fits your priorities.</p></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="demo-note"><b>DEMO DATA</b> &nbsp; Estimates use the sample routes and vehicle factors bundled with this project. They are not live traffic or measured emissions.</div>',
    unsafe_allow_html=True,
)
with st.sidebar:
    st.markdown("## Plan your journey")
    from_location = st.text_input("From", value="Kochi")
    to_location = st.text_input("To", value="Thrissur")
    vehicle_type = st.selectbox("Vehicle", vehicles["vehicle_type"].tolist())
    st.markdown("### Eco score weights")
    st.caption("Lower score is better. These weights control the demo recommendation.")
    fuel_weight = st.slider("Fuel", 0.0, 1.0, 0.30, 0.05)
    co2_weight = st.slider("CO₂", 0.0, 1.0, 0.30, 0.05)
    time_weight = st.slider("Travel time", 0.0, 1.0, 0.20, 0.05)
    traffic_weight = st.slider("Traffic", 0.0, 1.0, 0.10, 0.05)
    road_weight = st.slider("Road condition", 0.0, 1.0, 0.10, 0.05)
    find_button = st.button("🌱  FIND ECO ROUTE", type="primary", use_container_width=True)

weights = {
    "fuel": fuel_weight,
    "co2": co2_weight,
    "time": time_weight,
    "traffic": traffic_weight,
    "road": road_weight,
}

if find_button:
    if not from_location.strip() or not to_location.strip():
        st.error("Enter both a starting location and a destination.")
        st.stop()
    selected_routes = routes[
        routes["source"].str.casefold().eq(from_location.strip().casefold())
        & routes["destination"].str.casefold().eq(to_location.strip().casefold())
    ]
    if selected_routes.empty:
        st.warning("No sample routes are available for that location pair yet. Try Kochi to Thrissur.")
        st.stop()
    vehicle = vehicles.loc[vehicles["vehicle_type"] == vehicle_type].iloc[0]
    st.session_state["results"] = enrich_routes(selected_routes, vehicle, weights)
    st.session_state["vehicle"] = vehicle
    st.session_state["locations"] = (from_location.strip(), to_location.strip())

results = st.session_state.get("results")
if results is None:
    st.markdown("<div class='section-label'>Ready when you are</div>", unsafe_allow_html=True)
    st.info("Choose a journey in the sidebar and select Find Eco Route to compare the sample routes.")
else:
    recommendations = route_recommendations(results)
    fastest = recommendations["fastest"]
    eco = recommendations["eco"]
    source, destination = st.session_state["locations"]
    st.markdown("<div class='section-label'>Recommendation</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='route-banner'><small>🌱 Recommended eco route</small><strong>{eco['route_name']}</strong></div>",
        unsafe_allow_html=True,
    )
    metric_columns = st.columns(6)
    metrics = [
        ("Distance", f"{eco['distance_km']:.0f} km"),
    ("Travel time", f"{eco['travel_time_min']:.0f} min"),
    ("Fuel", f"{eco['fuel_litres']:.2f} L"),
    ("Estimated CO₂", f"{eco['co2_kg']:.2f} kg"),
        ("Traffic", eco["traffic_level"]),
        ("Eco score", f"{eco['eco_score']:.3f}"),
    ]
    for column, (label, value) in zip(metric_columns, metrics):
        column.metric(label, value)

    fuel_saved = max(0, (fastest["fuel_litres"] - eco["fuel_litres"]) / fastest["fuel_litres"] * 100)
    co2_saved = max(0, (fastest["co2_kg"] - eco["co2_kg"]) / fastest["co2_kg"] * 100) if fastest["co2_kg"] else 0
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("<div class='section-label'>Fastest vs eco route</div>", unsafe_allow_html=True)
        comparison = pd.DataFrame(
            {
                "Metric": ["Route", "Distance", "Time", "Fuel", "CO₂"],
                "Fastest route": [fastest["route_id"], f"{fastest['distance_km']:.0f} km", f"{fastest['travel_time_min']:.0f} min", f"{fastest['fuel_litres']:.2f} L", f"{fastest['co2_kg']:.2f} kg"],
                "Eco route": [eco["route_id"], f"{eco['distance_km']:.0f} km", f"{eco['travel_time_min']:.0f} min", f"{eco['fuel_litres']:.2f} L", f"{eco['co2_kg']:.2f} kg"],
            }
        )
        st.dataframe(comparison, hide_index=True, use_container_width=True)
        st.success(f"Compared with the fastest route: {fuel_saved:.1f}% estimated fuel saving and {co2_saved:.1f}% estimated CO₂ saving.")
    with right:
        st.markdown("<div class='section-label'>All candidate routes</div>", unsafe_allow_html=True)
        chart_data = results.set_index("route_id")[["fuel_litres", "co2_kg"]].rename(columns={"fuel_litres": "Fuel (L)", "co2_kg": "CO₂ (kg)"})
        st.bar_chart(chart_data, color=["#16845b", "#e9874d"])
    st.markdown("<div class='section-label'>Route details</div>", unsafe_allow_html=True)
    detail_columns = ["route_id", "route_name", "distance_km", "travel_time_min", "traffic_level", "road_condition", "fuel_litres", "co2_kg", "eco_score"]
    details = results[detail_columns].rename(columns={"route_id": "ID", "route_name": "Route", "distance_km": "Distance (km)", "travel_time_min": "Time (min)", "traffic_level": "Traffic", "road_condition": "Road", "fuel_litres": "Fuel (L)", "co2_kg": "CO₂ (kg)", "eco_score": "Eco score"})
    st.dataframe(details.style.format({"Fuel (L)": "{:.2f}", "CO₂ (kg)": "{:.2f}", "Eco score": "{:.3f}"}), hide_index=True, use_container_width=True)
st.markdown("<div class='section-label'>Exploration tools</div>", unsafe_allow_html=True)
traffic_tab, vision_tab, architecture_tab = st.tabs(["Traffic classification", "Road image analysis", "How this demo works"])
with traffic_tab:
    st.write("The current route file contains demo traffic features. A future K-Means model can learn clusters from these features without assuming cluster numbers have fixed meanings.")
    traffic_counts = routes["traffic_level"].value_counts().reindex(["LOW", "MEDIUM", "HIGH"], fill_value=0)
    st.bar_chart(traffic_counts)
    st.caption("Current labels are sample labels, not predictions from a trained model.")
with vision_tab:
    uploaded = st.file_uploader("Upload a road image", type=["jpg", "jpeg", "png"])
    if uploaded:
        st.image(uploaded, caption="Uploaded road image", use_container_width=True)
        try:
            from src.vision import detect_vehicles
            if st.button("Analyze vehicles", key="analyze_vehicles"):
                detections = detect_vehicles(uploaded)
                st.write(f"Detected vehicles: {len(detections)}")
                st.dataframe(pd.DataFrame(detections), hide_index=True, use_container_width=True)
        except ImportError:
            st.info("YOLO is an optional extension. Install Ultralytics before using image detection; the route planner does not require it.")
    else:
        st.caption("No image uploaded. No computer-vision result is being inferred.")
with architecture_tab:
    st.write("This version uses sample CSV routes, transparent fuel and CO₂ formulas, and a weighted eco score. K-Means, YOLO, road-damage detection, NetworkX, genetic optimization, and reinforcement learning are isolated as extension modules so they can be evaluated with real data later.")
    st.code("input -> sample routes -> fuel + CO2 estimates -> eco score -> comparison", language="text")
