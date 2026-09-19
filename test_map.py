from data.map import shortest_path


def test_shortest_path_from_arad_to_bucharest():
    route, distance = shortest_path("Arad", "Bucharest")
    assert route == ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert distance == 418


def test_shortest_path_from_oradea_to_bucharest():
    route, distance = shortest_path("Oradea", "Bucharest")
    # Optimal path uses the direct Oradea -> Sibiu (151 km) road
    assert route == ["Oradea", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert distance == 429


def test_shortest_path_from_timisoara_to_bucharest():
    route, distance = shortest_path("Timisoara", "Bucharest")
    # Optimal path via Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
    assert route == ["Timisoara", "Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert distance == 536
