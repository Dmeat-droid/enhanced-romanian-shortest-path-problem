import tkinter as tk
from tkinter import ttk, messagebox
from data.map import COORDINATES, ROADS
from core.algorithms import a_star_search, greedy_bfs
from core.heuristics import haversine_heuristic


class RomaniaMapGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Romanian Shortest Path Visualizer (A* vs Greedy BFS)")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)

        # Coordinate bounding box for canvas projection
        lats = [coord[0] for coord in COORDINATES.values()]
        lons = [coord[1] for coord in COORDINATES.values()]
        self.min_lat, self.max_lat = min(lats), max(lats)
        self.min_lon, self.max_lon = min(lons), max(lons)

        # State
        self.city_positions = {}
        self.cities = sorted(list(COORDINATES.keys()))

        self._setup_ui()
        self.draw_base_map()

    def _setup_ui(self):
        # Top Control Panel
        control_frame = ttk.LabelFrame(self.root, text=" Route Configuration ", padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Start City Selector
        ttk.Label(control_frame, text="Start City:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_combo = ttk.Combobox(control_frame, values=self.cities, state="readonly", width=15)
        self.start_combo.set("Arad")
        self.start_combo.grid(row=0, column=1, padx=5, pady=5)

        # Goal City Selector
        ttk.Label(control_frame, text="Goal City:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.goal_combo = ttk.Combobox(control_frame, values=self.cities, state="readonly", width=15)
        self.goal_combo.set("Bucharest")
        self.goal_combo.grid(row=0, column=3, padx=5, pady=5)

        # Algorithm Selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.algo_var = tk.StringVar(value="Both")
        algo_combo = ttk.Combobox(
            control_frame,
            textvariable=self.algo_var,
            values=["Both (Compare)", "A* Search", "Greedy BFS"],
            state="readonly",
            width=15,
        )
        algo_combo.grid(row=0, column=5, padx=5, pady=5)

        # Action Buttons
        btn_find = ttk.Button(control_frame, text="🔍 Find Path", command=self.run_search)
        btn_find.grid(row=0, column=6, padx=10, pady=5)

        btn_reset = ttk.Button(control_frame, text="↺ Reset", command=self.reset_map)
        btn_reset.grid(row=0, column=7, padx=5, pady=5)

        # Main Content: Canvas on Left, Results on Right
        content_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        content_pane.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Map Canvas Frame
        canvas_frame = ttk.Frame(content_pane)
        content_pane.add(canvas_frame, weight=3)

        self.canvas = tk.Canvas(canvas_frame, bg="#fcfcfc", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda event: self.redraw_all())

        # Results & Info Frame
        results_frame = ttk.LabelFrame(content_pane, text=" Path Summary & Details ", padding=10)
        content_pane.add(results_frame, weight=1)

        self.result_text = tk.Text(results_frame, wrap=tk.WORD, font=("Consolas", 10), width=35, bg="#f9f9f9")
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Bottom Legend / Status bar
        legend_frame = ttk.Frame(self.root, padding=5)
        legend_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=2)

        tk.Label(legend_frame, text="Legend: ", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        tk.Label(legend_frame, text="■ A* Path (Green)", fg="#2e7d32", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="■ Greedy BFS Path (Orange/Red)", fg="#d84315", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="● Cities (Blue)", fg="#1565c0", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)

    def _geo_to_canvas(self, lat: float, lon: float, w: int, h: int):
        pad_x = 60
        pad_y = 50
        scale_x = (w - 2 * pad_x) / (self.max_lon - self.min_lon)
        scale_y = (h - 2 * pad_y) / (self.max_lat - self.min_lat)

        x = pad_x + (lon - self.min_lon) * scale_x
        # Invert y because latitude increases upwards while screen y increases downwards
        y = h - pad_y - (lat - self.min_lat) * scale_y
        return x, y

    def draw_base_map(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w <= 1 or h <= 1:
            w, h = 600, 500

        # Calculate city coordinates on screen
        self.city_positions = {}
        for city, (lat, lon) in COORDINATES.items():
            self.city_positions[city] = self._geo_to_canvas(lat, lon, w, h)

        # Draw Roads (Edges)
        drawn_edges = set()
        for u, neighbors in ROADS.items():
            for v, dist in neighbors.items():
                edge_id = tuple(sorted([u, v]))
                if edge_id in drawn_edges:
                    continue
                drawn_edges.add(edge_id)

                x1, y1 = self.city_positions[u]
                x2, y2 = self.city_positions[v]

                # Draw road line
                self.canvas.create_line(x1, y1, x2, y2, fill="#cfd8dc", width=2, tags="road")

                # Draw road distance label
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_text(
                    mid_x, mid_y, text=str(dist), fill="#78909c", font=("Arial", 8), tags="road_label"
                )

        # Draw Cities (Nodes)
        r = 6
        for city, (x, y) in self.city_positions.items():
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#1976d2", outline="#0d47a1", width=2, tags="city_node")
            self.canvas.create_text(x, y - 13, text=city, font=("Arial", 9, "bold"), fill="#263238", tags="city_label")

    def redraw_all(self):
        self.draw_base_map()
        self.run_search()

    def reset_map(self):
        self.start_combo.set("Arad")
        self.goal_combo.set("Bucharest")
        self.algo_var.set("Both (Compare)")
        self.result_text.delete("1.0", tk.END)
        self.draw_base_map()

    def highlight_path(self, path: list, color: str, width: int, offset: int = 0):
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            x1, y1 = self.city_positions[u]
            x2, y2 = self.city_positions[v]
            self.canvas.create_line(
                x1 + offset, y1 + offset, x2 + offset, y2 + offset,
                fill=color, width=width, capstyle=tk.ROUND, tags="highlight_path"
            )

        # Highlight start and goal nodes
        if path:
            r = 8
            sx, sy = self.city_positions[path[0]]
            gx, gy = self.city_positions[path[-1]]
            self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill="#ffd600", outline="#f57f17", width=3, tags="highlight_node")
            self.canvas.create_oval(gx - r, gy - r, gx + r, gy + r, fill="#00e676", outline="#1b5e20", width=3, tags="highlight_node")

    def run_search(self):
        start = self.start_combo.get()
        goal = self.goal_combo.get()
        mode = self.algo_var.get()

        if not start or not goal:
            messagebox.showwarning("Input Error", "Please select both start and goal cities.")
            return

        if start == goal:
            messagebox.showinfo("Same Location", "Start and Goal are the same city!")
            return

        # Redraw background map to clear old highlighted paths
        self.draw_base_map()
        self.result_text.delete("1.0", tk.END)

        # Compute straight-line distance
        h_dist = haversine_heuristic(start, goal)
        summary = f"Route: {start} -> {goal}\n"
        summary += f"Haversine: {h_dist:.2f} km\n"
        summary += "=" * 32 + "\n\n"

        # 1. A* Search
        if mode in ["Both (Compare)", "A* Search"]:
            astar_route, astar_dist = a_star_search(start, goal)
            offset = 2 if mode == "Both (Compare)" else 0
            self.highlight_path(astar_route, color="#2e7d32", width=5, offset=offset)

            summary += "[A* Search (Optimal)]\n"
            summary += f"Distance: {astar_dist} km\n"
            summary += f"Hops: {len(astar_route) - 1}\n"
            summary += f"Path:\n {' -> '.join(astar_route)}\n\n"

        # 2. Greedy BFS
        if mode in ["Both (Compare)", "Greedy BFS"]:
            gbfs_route, gbfs_dist = greedy_bfs(start, goal)
            offset = -2 if mode == "Both (Compare)" else 0
            self.highlight_path(gbfs_route, color="#d84315", width=3, offset=offset)

            summary += "[Greedy BFS]\n"
            summary += f"Distance: {gbfs_dist} km\n"
            summary += f"Hops: {len(gbfs_route) - 1}\n"
            summary += f"Path:\n {' -> '.join(gbfs_route)}\n\n"

        # Difference analysis if comparing both
        if mode == "Both (Compare)":
            if astar_route == gbfs_route:
                summary += "-> Both algorithms found the EXACT same path!\n"
            else:
                diff = gbfs_dist - astar_dist
                summary += f"-> Greedy BFS took a {diff} km longer path than A*!\n"

        self.result_text.insert(tk.END, summary)


def main():
    root = tk.Tk()
    app = RomaniaMapGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

