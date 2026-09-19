from core.heuristics import haversine_heuristic

# Straight-line distance from Arad to Bucharest
h_arad = haversine_heuristic("Arad", "Bucharest")
print(f"h(Arad -> Bucharest) = {h_arad:.2f} km")
# Output: ~420.21 km