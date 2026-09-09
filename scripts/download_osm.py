"""Download a real OpenStreetMap driving graph for two places."""

import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.osm_graph import download_drive_graph


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", help="Starting place, for example Kochi")
parser.add_argument("destination", help="Destination place, for example Thrissur")
parser.add_argument(
    "--output",
    default="data/osm/route_network.graphml",
    help="Output GraphML path",
)
args = parser.parse_args()

output = Path(args.output)
download_drive_graph(args.source, args.destination, output)
print(f"Saved real OpenStreetMap graph to {output}")
