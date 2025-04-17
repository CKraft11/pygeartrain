```markdown
# pygeartrain

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python library for gear train calculations, visualizations, optimizations, and CAD profile export.

## Features

*   Symbolic calculation of gear ratios for various geartrain types.
*   Generation of 2D gear profiles (cycloidal, epi/hypo mix, involute - WIP).
*   Visualization and animation of geartrain kinematics using Matplotlib.
*   Export of gear profiles coordinates suitable for CAD import (e.g., SolidWorks).
*   Support for standard planetary, compound planetary (Wolfram), cycloidal, compound cycloidal, Nabtesco-style, and angular contact drives.

## Examples

Some examples of currently implemented gear trains:

**Compound Planetary (High Ratio)**
*(Image/GIF would go here if available)*
`./compound_planetary.gif`

**Compound Planetary (Printable Low Count)**
*(Image/GIF would go here if available)*
`./compound_planetary.png`

**Angular Contact Drive**
*(Image/GIF would go here if available)*
`./angular_contact.png`

**Cycloidal Drive**
*(Image/GIF would go here if available)*
`./cycloid.png`

## Installation & Environment Setup

This project uses Conda for environment management.

**Prerequisites:**
*   [Conda](https://docs.conda.io/en/latest/) (Miniconda is recommended: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html))
*   [Git](https://git-scm.com/) (for cloning the repository)

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> pygeartrain
    cd pygeartrain
    ```
    (Replace `<repository_url>` with the actual URL of the repository. Alternatively, download and extract the source code).

2.  **Create the Conda Environment:**
    Open your terminal or Anaconda Prompt in the `pygeartrain` directory (where `environment.yml` is located) and run:
    ```bash
    conda env create -f environment.yml
    ```
    *(Optional, faster alternative if you have Mamba installed: `mamba env create -f environment.yml`)*

3.  **Activate the Environment:**
    Each time you want to work with this project in a new terminal session, activate the environment:
    ```bash
    conda activate pygeartrain
    ```
    You should see `(pygeartrain)` appear at the beginning of your terminal prompt.

## Basic Usage: Calculating Ratios

You can define the kinematics of a geartrain and calculate its ratio symbolically:

```python
from pygeartrain.planetary import Planetary

# Define kinematics: Input='s' (sun), Output='c' (carrier), Fixed='r' (ring)
kinematics = Planetary('s', 'c', 'r')

# Print the kinematic definition and the calculated ratio formula
print(kinematics)
# >>> s/c: (R + S)/S
```

## Advanced Usage: Generating CAD Profiles for SolidWorks

A script is provided (let's assume you saved the one we developed as `generate_planetary_cad.py` in the main project directory) to export scaled helical or herringbone planetary gear profiles suitable for lofting in SolidWorks.

**1. Configuration:**

   Open the `generate_planetary_cad.py` script in a text editor. Modify the parameters in the "**User Defined Parameters**" section near the top:

   *   `TARGET_RING_DIAMETER_MM`: Set the desired outer diameter (in mm) for the final scaled ring gear. All other gears are scaled proportionally.
   *   `GEAR_THICKNESS_MM`: Set the total face width (along the Z-axis) for the gears.
   *   `HELIX_ANGLE_DEGREES`: Define the helix angle (in degrees) for one side of the gear tooth (used for both helix and herringbone).
   *   `GEAR_TYPE`: Choose `'helix'` for standard helical gears or `'herringbone'` for double-helical (V-shaped) gears.
   *   `R_teeth`, `P_teeth`, `S_teeth`: Set the tooth counts for the Ring, Planet, and Sun gears. Ensure they satisfy the planetary assembly condition: `R = S + 2*P`.
   *   `N_planets`: Set the number of planet gears around the sun.
   *   *(Optional)* `b_profile`: Adjust the epi/hypo cycloid mix ratio (0 to 1) for the tooth shape.
   *   *(Optional)* `CARRIER_PATH_POINTS`: Number of points for the exported circular carrier path file.
   *   *(Optional)* `CLOSE_POINT_TOLERANCE`, `SMALL_RADIUS_TOLERANCE`: Adjust point filtering sensitivity if needed.

**2. Running the Export Script:**

   Make sure the `pygeartrain` environment is active (`conda activate pygeartrain`). Run the script from the main project directory:

   ```bash
   python generate_planetary_cad.py
   ```

**3. Understanding the Output:**

   The script will create a directory named `output_helix` or `output_herringbone` containing several `.txt` files:

   *   **Gear Profile Curves:** 9 files for the gear teeth, 3 for each gear type (ring, planet, sun).
        *   `*_z0.txt`: The profile curve at the center plane (Z=0).
        *   `*_z_pos.txt`: The profile curve twisted for the +Z face (at Z = +thickness/2).
        *   `*_z_neg.txt`: The profile curve twisted for the -Z face (at Z = -thickness/2).
        *(The twist direction and type depend on the `HELIX_ANGLE_DEGREES` and `GEAR_TYPE` settings, with meshing hands automatically adjusted).*
   *   **Carrier Path:** 1 file:
        *   `carrier_path.txt`: A simple circle representing the path of the planet gear centers, useful for positioning planets in an assembly. Lies in the Z=0 plane.

   All coordinates in the files are in millimeters, scaled according to `TARGET_RING_DIAMETER_MM`.

**4. Importing into SolidWorks:**

   a.  Create a new SolidWorks Part file.
   b.  Import the 3 curves for **one gear** (e.g., `ring_21_z_neg.txt`, `ring_21_z0.txt`, `ring_21_z_pos.txt`):
       *   Go to **Insert > Curve > Curve Through XYZ Points**.
       *   **Browse** and select the first file (e.g., `_z_neg.txt`). Click **OK**.
       *   Repeat for the `_z0.txt` and `_z_pos.txt` files of the *same gear*. The curves should appear positioned correctly in 3D space.
   c.  Select the three imported curves for that gear in the FeatureManager Design Tree.
   d.  Create the gear body using **Insert > Boss/Base > Loft** (or **Insert > Surface > Loft**).
   e.  Check the loft connectors in the PropertyManager to ensure they connect corresponding points smoothly between the three profiles. Adjust if necessary. Click **OK**.
   f.  Repeat steps b-e for the Sun and Planet gears using their respective curve files.
   g.  **For the Planet:** After creating the single lofted planet gear body, use the **Circular Pattern** feature (**Insert > Pattern/Mirror > Circular Pattern**) to create `N_planets` instances around the part origin.
   h.  **Carrier Path (Optional):** Import `carrier_path.txt` onto a sketch on the Front Plane (Z=0) using **Insert > Curve > Curve Through XYZ Points**. This circle can be used as a construction reference for designing the physical carrier or for assembly mates.

## Animation

The geometry objects generated by the library (like `PlanetaryGeometry`) often have an `.animate()` method. You can call this in your script (after creating the `gear` object) to visualize the kinematic motion using Matplotlib.

```python
# Assuming 'gear' is a created PlanetaryGeometry object
# gear.animate() # Call this instead of static plotting
# plt.show() # Not needed if calling animate()
```

*Note: The animation shows the **unscaled** gear profiles to verify meshing and relative speeds based on the kinematics.*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```