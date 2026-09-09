# EcoRoute Data Sources

## OpenStreetMap road network

- **Provider:** OpenStreetMap contributors
- **URL:** https://www.openstreetmap.org/
- **Access library:** OSMnx
- **Purpose:** Geocoding, drivable road graph, road nodes, road segments, distances, and OSM speed/travel-time attributes
- **Local file:** `data/osm/route_network.graphml`
- **Format:** GraphML
- **License:** OpenStreetMap data is available under the Open Database License (ODbL). See https://www.openstreetmap.org/copyright.
- **How used:** The downloader requests a drivable graph around the selected place pair. EcoRoute then snaps each place to the nearest graph node and computes a shortest-distance route.
- **Important limitation:** OSM does not provide live traffic, measured fuel use, or measured emissions for this project. Those quantities must come from separate documented sources.

## BDD100K

- **Provider:** Berkeley DeepDrive
- **URL:** https://www.vis.xyz/bdd100k/
- **Purpose:** Vehicle detection and road-scene understanding
- **Local folder:** `data/bdd100k/`
- **Status:** Not downloaded. Official access terms and licensing must be checked before obtaining it.

## RDD2022

- **Provider:** Sekilab / RoadDamageDetector project
- **URL:** https://github.com/sekilab/RoadDamageDetector
- **Purpose:** Road-damage detection
- **Local folder:** `data/rdd2022/`
- **Status:** Not downloaded. Dataset structure, image counts, and license will be recorded from the official distribution before use.

## Traffic dataset

No external traffic dataset has been selected yet. The bundled `data/routes.csv` is TEST DATA only and must not be used as a final experimental dataset. Before the traffic model phase, at least three real candidates will be compared by source, license, features, and accessibility.

## Fuel and emissions data

No authoritative external fuel/emissions source has been added yet. The current vehicle CSV and adjustment factors are TEST DATA and estimates only. A documented government, standards-body, or peer-reviewed source is required before final experiments.
