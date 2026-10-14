"""Integration tests for the Streamlit dashboard using AppTest."""

import pytest
from streamlit.testing.v1 import AppTest


def test_app_default_render():
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    assert not at.exception


def test_app_navigation_pages():
    pages = [
        "🧭 Route Planner",
        "🚦 Traffic Analysis",
        "🚗 Vehicle Detection",
        "🛣️ Road Condition",
        "⚖️ Route Comparison",
        "📈 Model Performance",
        "ℹ️ About Project",
    ]
    for p in pages:
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        at.sidebar.radio[0].set_value(p).run()
        assert not at.exception, f"Failed on page: {p}"


def test_app_form_submit():
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    at.text_input(key="origin_input").set_value("Kochi").run()
    at.text_input(key="dest_input").set_value("Thrissur").run()
    at.selectbox(key="vehicle_input").select("Diesel Car").run()
    at.button[0].click().run()
    assert not at.exception
