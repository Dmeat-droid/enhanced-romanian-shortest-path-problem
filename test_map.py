from data.map import shortest_path


def test_shortest_path_from_arad_to_bucharest():
    route, distance = shortest_path("Arad", "Bucharest")
    assert route == ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert distance == 418


def test_shortest_path_from_oradea_to_bucharest():
    route, distance = shortest_path("Oradea", "Bucharest")
    assert route == ["Oradea", "Zerind", "Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert distance == 564
