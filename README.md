# Photonic Crystal Visualizer

An interactive web-based explorer for visualizing 2D photonic crystal structures and lattices. Built with Python, Dash, Plotly, and Shapely, this application allows users to interactively construct, tune, and analyze 2D crystal lattices by placing different species (shapes) at various symmetry points.

## Features

- **Interactive Visualization:** View the crystal lattice in real-time, constructed with plotly.
- **Lattice Types:** Toggle between 2D Hexagonal and Square crystal structures.
- **Multiple Species:** Add different species/materials mapped to specific symmetry points (Wyckoff positions).
- **Geometric Controls:** Dynamically adjust the radius/size of the placed shapes, and tune the variable $x$ parameter for certain Wyckoff positions.
- **Area Statistics:** Calculates and displays fractional area statistics of the placed structures within the unit cell, leveraging `shapely` for boolean geometry operations.

## 2D Crystal Structures and Wyckoff Positions

This application supports two of the fundamental 2D Bravais lattices/plane groups, each with their own standardized high-symmetry Wyckoff positions:

### 1. Hexagonal Lattice (p6mm)
The hexagonal lattice is defined by vectors of equal length separated by an angle of 120°.

**Supported Wyckoff Positions:**
- **1a:** Origin - A single point at $(0, 0)$
- **2b:** Honeycomb - Two points at $(1/3, 1/3)$ and $(2/3, 2/3)$
- **3c:** Kagome - Three points at $(1/2, 0)$, $(0, 1/2)$, and $(1/2, 1/2)$
- **6d:** Primary Hexamer - A 6-point variable configuration $x$, default $x=0.25$
- **6e:** Secondary Hexamer - A 6-point variable configuration $x$, default $x=0.15$

### 2. Square Lattice (p4mm)
The square lattice is defined by orthogonal vectors of equal length.

**Supported Wyckoff Positions:**
- **1a:** Origin - A single point at $(0, 0)$
- **1b:** Center - A single point at $(1/2, 1/2)$
- **2c:** Edges - Two points at $(1/2, 0)$ and $(0, 1/2)$
- **4d:** Diagonals - A 4-point variable configuration $x$, default $x=0.25$
- **4e:** Axes - A 4-point variable configuration $x$, default $x=0.25$

## Installation and Running

1. Clone the repository and navigate into the directory.
2. Install the required dependencies:
   ```bash
   pip install dash plotly shapely
   ```
3. Run the Dash application:
   ```bash
   python app.py
   ```
4. Open the application in your local web browser (default usually `http://127.0.0.1:8050`).
