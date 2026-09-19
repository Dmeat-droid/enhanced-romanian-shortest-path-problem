import math
from typing import Tuple
from data.map import COORDINATES

EARTH_RADIUS_KM = 6371.0

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
  lat1, lon1 = coord1
  lat2, lon2 = coord2

  phi1 = math.radians(lat1)
  phi2 = math.radians(lat2)
  delta_phi = math.radians(lat2 - lat1)
  delta_lambda = math.radians(lon2 - lon1)

  a = (
    math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
  )

  c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

  return EARTH_RADIUS_KM * c

def haversine_heuristic(current_city: str, goal_city: str) -> float:
  if current_city not in COORDINATES:
    raise KeyError(f"Coordinates for city '{current_city}' not found")
  if goal_city not in COORDINATES:
    raise KeyError(f"Coordinates for city '{goal_city}' not found.")
  return haversine_distance(COORDINATES[current_city], COORDINATES[goal_city])