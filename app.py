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
    :root { --ink:#153332; --muted:#637472; --mint:#dff3e9; --green:#16845b; --green-dark:#0d5c40; --orange:#e9874d; --line:#dce8e3; --surface:#ffffff; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    [data-testid="stAppViewContainer"] { background: #f7faf8; }
    [data-testid="stHeader"] { background: transparent; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
    h1 { font-size: clamp(2.1rem, 5vw, 4.2rem); line-height: 1.02; }
    [data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 15px; box-shadow: 0 5px 18px rgba(21,51,50,.05); }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); }
    .hero { background: linear-gradient(120deg, #dff3e9 0%, #f7faf8 68%); border: 1px solid #cbe6d9; border-radius: 16px; padding: 30px 34px; margin-bottom: 22px; box-shadow: 0 8px 26px rgba(21,51,50,.06); }
    .eyebrow { color: var(--green); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: .78rem; }
    .demo-note { color: #71502d; background: #fff1dc; border-left: 4px solid var(--orange); padding: 10px 13px; border-radius: 4px; font-size: .9rem; }
    .route-banner { background: linear-gradient(120deg, var(--green-dark), var(--ink)); color: white; border-radius: 14px; padding: 20px 22px; box-shadow: 0 10px 26px rgba(13,92,64,.18); }
    .route-banner small { color: #acd8c4; text-transform: uppercase; letter-spacing: .08em; }
    .route-banner strong { display:block; font-size: 1.3rem; margin-top: 3px; }
    .section-label { color: var(--muted); text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; font-weight: 700; margin: 22px 0 8px; }
    .search-card, .panel { background: white; border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; box-shadow: 0 6px 20px rgba(21,51,50,.05); }
    .search-card { margin-bottom: 18px; }
    .status-pill { display:inline-block; padding: 4px 9px; border-radius: 999px; background: var(--mint); color: var(--green-dark); font-weight: 700; font-size: .78rem; }
    .muted-note { color: var(--muted); font-size: .9rem; }
    @media (max-width: 700px) { .hero { padding: 24px 20px; } h1 { font-size: 2.5rem; } }
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
    '<div class="hero"><div class="eyebrow">🌱 EcoRoute · Route intelligence for everyday travel</div>'
    '<h1>Smarter routes.<br>Lower emissions.</h1>'
    '<p>Find routes that balance travel time, fuel consumption and environmental impact.</p></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="demo-note"><b>DEMO DATA</b> &nbsp; Estimates use the sample routes and vehicle factors bundled with this project. They are not live traffic or measured emissions.</div>',
    unsafe_allow_html=True,
)
with st.sidebar:
    st.markdown("## EcoRoute")
    st.caption("Transparent route planning with sample data")
    page = st.radio("Navigate", ["Route planner", "Traffic analysis", "Vehicle detection", "Road condition", "Route comparison", "Model performance", "About"], label_visibility="collapsed")
    st.divider()
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

st.markdown("<div class='search-card'>", unsafe_allow_html=True)
st.markdown("### Plan your journey")
search_columns = st.columns([1, 1, 1.05])
with search_columns[0]:
    from_location = st.text_input("📍 From", value="Kochi")
with search_columns[1]:
    to_location = st.text_input("🏁 Destination", value="Thrissur")
with search_columns[2]:
    vehicle_type = st.selectbox("🚗 Vehicle", vehicles["vehicle_type"].tolist())
st.markdown("</div>", unsafe_allow_html=True)

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
if page == "Traffic analysis":
    st.markdown("<div class='section-label'>Live from the route dataset</div>", unsafe_allow_html=True)
    st.header("🚦 Traffic analysis")
    traffic_counts = routes["traffic_level"].value_counts().reindex(["LOW", "MEDIUM", "HIGH"], fill_value=0)
    traffic_columns = st.columns(4)
    traffic_columns[0].metric("Routes sampled", len(routes))
    traffic_columns[1].metric("Vehicle count", f"{routes['vehicle_count'].mean():.0f} avg")
    traffic_columns[2].metric("Average speed", f"{routes['average_speed_kmh'].mean():.0f} km/h")
    traffic_columns[3].metric("Traffic density", f"{routes['traffic_density'].mean():.2f}")
    traffic_left, traffic_right = st.columns([1, 1.2])
    with traffic_left:
        st.markdown("#### Traffic levels")
        st.bar_chart(traffic_counts, color="#16845b")
    with traffic_right:
        st.markdown("#### Route-level observations")
        st.dataframe(routes[["route_id", "traffic_level", "vehicle_count", "average_speed_kmh", "traffic_density"]], hide_index=True, use_container_width=True)
elif page == "Vehicle detection":
    st.markdown("<div class='section-label'>Optional computer vision extension</div>", unsafe_allow_html=True)
    st.header("🚗 Vehicle detection")
    st.caption("Upload a road image to run the bundled YOLO integration when Ultralytics and model weights are available.")
    uploaded = st.file_uploader("Upload a road image", type=["jpg", "jpeg", "png"])
    if uploaded:
        image_left, image_right = st.columns(2)
        with image_left:
            st.image(uploaded, caption="Original image", use_container_width=True)
        with image_right:
            try:
                from src.vision import detect_vehicles
                if st.button("Analyze vehicles", key="analyze_vehicles", type="primary"):
                    with st.spinner("Running vehicle detection..."):
                        detections = detect_vehicles(uploaded)
                    st.metric("Vehicle count", len(detections))
                    st.dataframe(pd.DataFrame(detections), hide_index=True, use_container_width=True)
            except ImportError:
                st.info("The vehicle detection model is not available. Install Ultralytics and provide model weights to enable it.")
    else:
        st.info("Upload a road image to begin analysis.")
elif page == "About":
    st.markdown("<div class='section-label'>About this demo</div>", unsafe_allow_html=True)
    st.header("A transparent route planning experiment")
    st.write("EcoRoute currently uses the bundled sample CSV routes, vehicle factors, fuel and CO₂ formulas, and a weighted eco score. Optional modules for OSM routing, K-Means, YOLO, road damage, genetic optimization, and reinforcement learning remain separate from this interface.")
    st.warning("This demo does not contain live traffic, measured emissions, route coordinates, a bundled road-damage model, or benchmark performance results. Those outputs are intentionally not shown as if they were available.")
elif page == "Road condition":
    st.markdown("<div class='section-label'>Road image analysis</div>", unsafe_allow_html=True)
    st.header("🛣 Road condition analysis")
    st.info("No road-damage model or labeled damage output is bundled with this project yet. Upload processing is intentionally unavailable until a real model is connected.")
elif page == "Model performance":
    st.markdown("<div class='section-label'>Evaluation workspace</div>", unsafe_allow_html=True)
    st.header("📈 Model performance")
    st.info("No benchmark metrics are stored in the current project. Performance cards will appear here once real evaluation outputs are available.")
elif page == "Route comparison":
    st.markdown("<div class='section-label'>Fastest vs eco-friendly</div>", unsafe_allow_html=True)
    st.header("⚡ Route comparison")
    if results is None:
        st.info("Run a route search to compare the fastest and eco-recommended candidates.")
    else:
        comparison_recommendations = route_recommendations(results)
        comparison_columns = st.columns(2)
        for column, title, route_key in zip(comparison_columns, ["⚡ Fastest route", "🌱 Eco route"], ["fastest", "eco"]):
            route = comparison_recommendations[route_key]
            with column:
                st.markdown(f"#### {title}")
                st.metric("Distance", f"{route['distance_km']:.0f} km")
                st.metric("Travel time", f"{route['travel_time_min']:.0f} min")
                st.metric("Fuel", f"{route['fuel_litres']:.2f} L")
                st.metric("CO₂", f"{route['co2_kg']:.2f} kg")
else:
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
    st.markdown("<div class='section-label'>Map view</div>", unsafe_allow_html=True)
    st.info("A geographic map is not shown because the current route dataset contains no source, destination, or road-segment coordinates. This avoids inventing map positions.")
