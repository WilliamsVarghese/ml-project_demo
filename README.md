# EcoRoute

EcoRoute is a Streamlit application for comparing driving routes by travel time, fuel use, and estimated CO2 emissions.

## What works now

The dashboard includes real OpenStreetMap route generation, plus a clearly labeled TEST DATA comparison while external traffic, vehicle, and emissions sources are being added. It also includes fuel and road-condition adjustments, estimated CO2, a configurable weighted eco score, fastest-versus-eco comparison, savings, charts, and optional image analysis.

All route and traffic values are clearly marked demo data. Fuel and CO2 values are estimates, not measurements from a vehicle or emissions monitor.

## Installation

### 1. Install Python Packages
```powershell
& "C:/Program Files/Python313/python.exe" -m pip install -r requirements.txt
```

### 2. Run the Application
```powershell
& "C:/Program Files/Python313/python.exe" -m streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure
```
EcoRoute/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md
├── data/                 # TEST DATA and downloaded real data
│   └── osm/              # OpenStreetMap GraphML
├── models/               # Trained models when available
├── src/                  # Calculation and extension modules
└── notebooks/            # Exploration notebooks
```

See [docs/datasets.md](docs/datasets.md) for source URLs, licensing, and current data availability.

## Development Phases

- [x] **PHASE 1-7:** Core dashboard, sample route calculations, and UI
- [x] **PHASE 8-14:** Extension module interfaces added
- [ ] Live data, trained K-Means model, YOLO weights, and RDD2022 evaluation

## Calculation model

Base fuel is `distance / vehicle efficiency`, adjusted by traffic and road-condition factors. Estimated CO2 is fuel multiplied by the vehicle's configurable CO2-per-litre factor. The eco score normalizes fuel, CO2, and time, then adds traffic and road-condition penalties.

## Real OpenStreetMap routing

Install the dependencies and download a real driving graph for a place pair:

```powershell
& "C:/Program Files/Python313/python.exe" -m pip install -r requirements.txt
& "C:/Program Files/Python313/python.exe" scripts/download_osm.py Kochi Thrissur
```

The downloader uses OpenStreetMap geocoding and road data through OSMnx, then saves `data/osm/route_network.graphml`. The downloaded graph is real geographic data, not a manually authored route. OpenStreetMap data is provided under the ODbL and must be attributed when redistributed.

## Advanced extensions

`src/traffic.py`, `vision.py`, `road_damage.py`, `graph.py`, `genetic_optimizer.py`, and `rl_agent.py` provide isolated extension points. No trained model, live traffic feed, RDD2022 dataset, or YOLO detection result is claimed until those assets are installed and evaluated.

## Validation

Python compilation, sample calculation tests, and Streamlit's built-in app testing API pass for the current dashboard.
