# 🗺️ Enhanced Romanian Shortest Path Problem

Proyek ini mengimplementasikan pencarian rute terpendek pada permasalahan klasik **Romania Map Problem** menggunakan pendekatan kecerdasan artifisial (Informed Search) berbasis koordinat geografis nyata (GPS).

---

## 📌 Fitur Utama

- **Haversine Heuristic ($h(n)$)**: Menghitung jarak garis lurus *great-circle* pada permukaan bumi menggunakan koordinat lintang (*latitude*) dan bujur (*longitude*). Heuristik ini terbukti *admissible* ($h(n) \le h^*(n)$).
- **A\* Search**: Algoritma pencarian optimal yang meminimalkan $f(n) = g(n) + h(n)$, menjamin penemuan rute dengan jarak total terpendek.
- **Greedy Best-First Search (GBFS)**: Algoritma pencarian yang hanya memprioritaskan jarak perkiraan ke tujuan $f(n) = h(n)$.
- **Interactive GUI Visualizer**: Visualisasi graf peta Romania interaktif berbasis `tkinter` yang menampilkan jalur $A^*$ (hijau) dan Greedy BFS (oranye/merah) secara berdampingan.
- **Unit Testing**: Pengujian otomatis menggunakan `pytest` untuk memastikan kebenaran rute dan jarak optimal.

---

## 📁 Struktur Direktori

```text
├── core/
│   ├── algorithms.py     # Implementasi A* Search dan Greedy Best-First Search
│   └── heuristics.py     # Implementasi Haversine Formula untuk jarak geografis
├── data/
│   └── map.py            # Dataset koordinat kota dan graf bobot jalan
├── gui.py                # Antarmuka visual interaktif berbasis Tkinter
├── main.py               # Entry point utama untuk menjalankan aplikasi
├── test_map.py           # Unit testing rute optimal
└── README.md             # Dokumentasi proyek
```

---

## 🚀 Cara Menjalankan Program

### Prasyarat:
- Python 3.8 atau lebih baru.
- **Tidak ada library eksternal yang wajib di-install** (menggunakan library bawaan Python: `tkinter`, `heapq`, `math`, `typing`).

### 1. Menjalankan Visualizer (GUI):
Jalankan perintah berikut di terminal:
```bash
python main.py
```
*Atau:*
```bash
python gui.py
```

### 2. Menjalankan Unit Testing:
Untuk memverifikasi kebenaran algoritma secara otomatis:
```bash
pytest test_map.py
```

---

## 📊 Hasil dan Analisis Perbandingan

### 1. Rute `Arad` $\to$ `Bucharest`
- **Jarak Heuristik Garis Lurus (Haversine)**: $422.54\text{ km}$
- **A\* Search (Optimal)**:
  - Rute: `Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest`
  - Jarak: **$418\text{ km}$**
- **Greedy BFS**:
  - Rute: `Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest`
  - Jarak: **$418\text{ km}$**
  - *Catatan: Pada data GPS riil, Rimnicu Vilcea memang secara geografis lebih dekat ke Bucharest dibandingkan Fagaras, sehingga Greedy BFS juga menemukan rute ini.*

### 2. Rute `Timisoara` $\to$ `Bucharest` *(Kasus Suboptimal Greedy BFS)*
- **A\* Search (Optimal)**:
  - Rute: `Timisoara -> Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest`
  - Jarak: **$536\text{ km}$**
- **Greedy BFS (Suboptimal)**:
  - Rute: `Timisoara -> Lugoj -> Mehadia -> Drobeta -> Craiova -> Pitesti -> Bucharest`
  - Jarak: **$615\text{ km}$**
  - *Analisis: Greedy BFS terjebak memilih rute selatan (Lugoj) karena jarak garis lurus Lugoj ke Bucharest lebih pendek daripada Arad ke Bucharest, meskipun total jarak jalan raya yang ditempuh justru lebih panjang $79\text{ km}$.*

---

## 📝 Kesimpulan

1. **Haversine Formula** menghasilkan estimasi jarak yang konsisten dan *admissible*, sehingga cocok digunakan sebagai fungsi heuristik $h(n)$ pada pencarian rute berbasis peta dunia nyata.
2. **A\* Search** selalu menjamin solusi rute terpendek yang optimal karena mempertimbangkan akumulasi biaya yang telah ditempuh ($g(n)$) bersama dengan estimasi sisa jarak ($h(n)$).
3. **Greedy BFS** dapat menghasilkan rute yang suboptimal atau lebih panjang karena hanya mengejar simpul dengan nilai $h(n)$ terkecil tanpa memperhitungkan biaya perjalanan sebelumnya.

