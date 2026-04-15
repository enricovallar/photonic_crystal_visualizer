# Photonic Crystal Visualizer

An interactive web-based explorer for visualizing 2D photonic crystal structures and lattices. Built with Python, Dash, Plotly, and Shapely, this application allows users to interactively construct, tune, and analyze 2D crystal lattices by placing different species (shapes) at various symmetry points.

## Features

- **Interactive Visualization:** View the crystal lattice in real-time, constructed with plotly.
- **Lattice Types:** Toggle between 2D Hexagonal and Square crystal structures.
- **Multiple Species:** Add different species/materials mapped to specific symmetry points (Wyckoff positions).
- **Geometric Controls:** Dynamically adjust the radius/size of the placed shapes, and tune the variable $x$ parameter for certain Wyckoff positions.
- **Area Statistics:** Calculates and displays fractional area statistics of the placed structures within the unit cell, leveraging `shapely` for boolean geometry operations.

## Understanding Wyckoff Positions

In crystallography, **Wyckoff positions** determine the precise locations of objects (like atoms, meta-atoms, or geometric holes) within a crystal's unit cell, dictated by the crystal's space group symmetry. They tell us exactly where we can place shapes inside the lattice so that the overall macroscopic symmetric properties of the crystal are perfectly preserved. 

### Wyckoff Nomenclature

Wyckoff positions are labelled using a number followed by a letter (e.g., **1a**, **2b**, **6d**). 
- **The number (Multiplicity):** Indicates the number of symmetrically equivalent points that are generated in a single unit cell. For example, a multiplicity of '6' means placing an object at this position yields exactly 6 identical objects within the unit cell due to the symmetry of the lattice.
- **The letter (Wyckoff Letter):** An alphabetical label (a, b, c, d...) assigned in ascending order starting from the position with the highest site symmetry. It serves as a unique identifier for that specific geometric arrangement within the space group.

### Types of Positions

- **Fixed Positions (e.g., 1a, 2b):** These correspond to exact, non-movable points of high symmetry (like the origin or exact center). Placing objects here typically requires just knowing the size (radius).
- **Variable Positions (e.g., 6d, 4e):** These involve a degree of freedom, typically denoted by a fractional coordinate scaling parameter $x$. Changing this parameter moves the points symmetrically along specific axes or diagonal lines, allowing for continuously tunable structures (like expanding hexamers or rotating patterns) while still preserving the lattice's fundamental symmetry.

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

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable, and reproducible environment management on Windows.

1. Clone the repository and navigate into the directory.
2. Sync the environment and install dependencies:
   ```bash
   uv sync
   ```
3. Run the Dash application using `uv`:
   ```bash
   uv run python app.py
   ```
4. Open the application in your local web browser (default usually `http://127.0.0.1:8050`).

## Deployment as an Executable (.exe)

This project can be fully packaged into a standalone Windows executable (`.exe`) via [PyInstaller](https://pyinstaller.org/). This compiles your Python code and its dependencies so end-users without Python can run the app locally.

The `uv sync` command already installed `pyinstaller` into your locked environment.

1. Build the application using `uv run` to ensure it uses the reproducible environment. You can use the pre-existing spec file if there is one configured:
   ```bash
   uv run pyinstaller "Photonic Crystal Visualizer.spec"
   ```
   Or explicitly build from the main app file:
   ```bash
   uv run pyinstaller --name "Photonic Crystal Visualizer" --onefile app.py
   ```
2. After the build completes, the generated executable will be placed inside the `dist/` directory. 
3. Running the `.exe` will launch the Dash server in the background. Users will still need to navigate to `http://127.0.0.1:8050` in their web browser to view the application interface.
