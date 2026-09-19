import heapq
from typing import Callable, Dict, List, Optional, Tuple
from data.map import ROADS
from core.heuristics import haversine_heuristic


def _reconstruct_path(came_from: Dict[str, Optional[str]], current: str) -> List[str]:
    """Rebuilds the path from start to goal following parent pointers."""
    path = []
    curr: Optional[str] = current
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path


def greedy_bfs(
    start: str,
    goal: str,
    heuristic: Callable[[str, str], float] = haversine_heuristic,
) -> Tuple[List[str], int]:
    """
    Greedy Best-First Search:
    Prioritizes nodes solely by h(n) (estimated distance to goal).
    Returns (path, total_distance).
    """
    # Priority queue stores: (h_cost, current_node, g_cost)
    frontier = [(heuristic(start, goal), start, 0)]
    visited = set()
    came_from: Dict[str, Optional[str]] = {start: None}

    while frontier:
        _, current, g_cost = heapq.heappop(frontier)

        if current == goal:
            return _reconstruct_path(came_from, current), g_cost

        if current in visited:
            continue
        visited.add(current)

        for neighbor, distance in ROADS.get(current, {}).items():
            if neighbor not in visited and neighbor not in came_from:
                came_from[neighbor] = current
                h_val = heuristic(neighbor, goal)
                heapq.heappush(frontier, (h_val, neighbor, g_cost + distance))

    return [], 0


def a_star_search(
    start: str,
    goal: str,
    heuristic: Callable[[str, str], float] = haversine_heuristic,
) -> Tuple[List[str], int]:
    """
    A* Search:
    Prioritizes nodes by f(n) = g(n) + h(n).
    Guaranteed to find the optimal shortest path if h(n) is admissible.
    Returns (path, total_distance).
    """
    # Priority queue stores: (f_cost, g_cost, current_node)
    frontier = [(heuristic(start, goal), 0, start)]
    came_from: Dict[str, Optional[str]] = {start: None}
    g_costs: Dict[str, int] = {start: 0}

    while frontier:
        f_cost, g_cost, current = heapq.heappop(frontier)

        if current == goal:
            return _reconstruct_path(came_from, current), g_cost

        if g_cost > g_costs.get(current, float("inf")):
            continue

        for neighbor, distance in ROADS.get(current, {}).items():
            new_g = g_cost + distance

            if new_g < g_costs.get(neighbor, float("inf")):
                g_costs[neighbor] = new_g
                came_from[neighbor] = current
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (new_f, new_g, neighbor))

    return [], 0