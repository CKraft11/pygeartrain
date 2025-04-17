import matplotlib.pyplot as plt
import numpy as np
import os

# Import the classes for single-stage planetary gears
from pygeartrain.planetary import Planetary, PlanetaryGeometry

# --- User Defined Parameters ---
TARGET_RING_DIAMETER_MM = 70.0  # Desired outer diameter for the ring gear in mm
CLOSE_POINT_TOLERANCE = 1e-7    # Tolerance for removing duplicate/close points

# --- Parameters derived from the "Blue" Stage (Stage 2) ---
R_teeth = 21
P_teeth = 6
S_teeth = 9
N_planets = 6
b_profile = 0.66

# --- Define Single-Stage Planetary Kinematics ---
kinematics = Planetary('s', 'c', 'r')

# --- Define Geometry ---
G = (R_teeth, P_teeth, S_teeth)

# --- Create the Gear Geometry Object ---
gear = PlanetaryGeometry.create(
    kinematics=kinematics,
    G=G,
    N=N_planets,
    b=b_profile
)

# --- Print Gear Information (Verification) ---
print("Generated Single-Stage Planetary Gear Configuration:")
print(gear)
print(f"\nInput: {gear.kinematics.input}")
print(f"Output: {gear.kinematics.output}")
print(f"Fixed: {gear.kinematics.aux[0]}")
print(f"Calculated Ratio (Symbolic): {gear.ratio}")
print(f"Calculated Ratio (Numeric): {gear.ratio_f:.4f}")

# --- Get Base Profiles (Unscaled) ---
base_ring_profile, base_planet_profile, base_sun_profile, _ = gear.generate_profiles

# --- Calculate Scaling Factor ---
# Find the maximum radius of the unscaled ring gear
unscaled_ring_vertices = base_ring_profile.vertices
radii = np.linalg.norm(unscaled_ring_vertices, axis=1)
max_radius_unscaled = np.max(radii)

# Calculate the scale factor needed
target_radius = TARGET_RING_DIAMETER_MM / 2.0
if max_radius_unscaled <= 1e-9: # Avoid division by zero if profile is just the origin
    print("Warning: Unscaled ring gear has zero radius. Cannot calculate scale factor.")
    scale_factor = 1.0
else:
    scale_factor = target_radius / max_radius_unscaled

print(f"\nTarget Ring Radius: {target_radius:.4f} mm")
print(f"Max Unscaled Ring Radius: {max_radius_unscaled:.4f}")
print(f"Calculated Scale Factor: {scale_factor:.6f}")

# --- Prepare Data for SolidWorks Export ---

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Output directory already exists: {output_dir}")


# Function to prepare and save vertices for SolidWorks (Scaling + Duplicate Check)
def save_profile_for_solidworks(profile, gear_name, tooth_count, scale_factor):
    """Scales vertices, removes *consecutive* close points, ensures loop closure,
       adds Z=0, and saves to a text file in space-delimited format without headers."""
    if profile is None or len(profile.vertices) < 3: # Need at least 3 points for a meaningful loop
        print(f"Warning: Not enough vertices found for {gear_name}. Skipping export.")
        return

    # 1. Scale the profile
    vertices_2d_scaled = profile.vertices * scale_factor

    # 2. Filter consecutive points that are too close
    #    Start with the first point, iterate through the rest
    filtered_points = [vertices_2d_scaled[0]]
    for i in range(len(vertices_2d_scaled) - 1):
        point_current = filtered_points[-1] # Compare against the *last added* filtered point
        point_next = vertices_2d_scaled[i+1]
        distance = np.linalg.norm(point_next - point_current)
        if distance > CLOSE_POINT_TOLERANCE:
            filtered_points.append(point_next)

    print(f"{gear_name}: Original points (scaled): {len(vertices_2d_scaled)}, Points after consecutive filter: {len(filtered_points)}")

    if len(filtered_points) < 3:
         print(f"Warning: Not enough vertices after filtering close points for {gear_name}. Skipping export.")
         return

    # 3. Ensure loop closure: Check if the last filtered point is close to the first.
    first_point = filtered_points[0]
    last_point = filtered_points[-1]
    if np.linalg.norm(last_point - first_point) > CLOSE_POINT_TOLERANCE:
        print(f"    -> Forcing closure by appending first point to the end for {gear_name}.")
        filtered_points.append(first_point) # Add the first point again to close the loop

    filtered_points_arr = np.array(filtered_points)

    # 4. Add a Z column of zeros
    vertices_3d_final = np.column_stack((
        filtered_points_arr[:, 0],
        filtered_points_arr[:, 1],
        np.zeros(filtered_points_arr.shape[0])
    ))

    # 5. Define the output filename
    filename = f"{gear_name}_{tooth_count}.txt"
    filepath = os.path.join(output_dir, filename)

    # 6. Save the data using numpy.savetxt (Space delimited, high precision, no header)
    np.savetxt(filepath, vertices_3d_final, fmt='%.8f', delimiter=' ')
    print(f"Exported {gear_name} profile vertices to: {filepath} (Scaled, Filtered, Closed, SolidWorks Format)")

# --- Save Scaled and Filtered Gear Profiles ---
print("\nExporting profiles...")
save_profile_for_solidworks(base_ring_profile, "ring", R_teeth, scale_factor)
save_profile_for_solidworks(base_planet_profile, "planet", P_teeth, scale_factor)
save_profile_for_solidworks(base_sun_profile, "sun", S_teeth, scale_factor)

# --- Plot the Scaled Gear Profiles (Optional Visualization) ---
# Note: The plotting part now uses the *unscaled* profiles arranged,
#       so it won't reflect the TARGET_RING_DIAMETER_MM visually unless modified.
#       You could modify it to plot the scaled versions if needed for verification.
print("\nGenerating original scale plot for visual reference...")
fig, ax = plt.subplots(figsize=(8, 8))

phase = 0
# Arrange uses the *unscaled* geometry by default
ring_profile_arranged, planet_profiles_arranged, sun_profile_arranged, _ = gear.arrange(phase)

plot_color = 'b'
ring_profile_arranged.plot(ax=ax, color=plot_color)
sun_profile_arranged.plot(ax=ax, color=plot_color)
for planet in planet_profiles_arranged:
    planet.plot(ax=ax, color=plot_color)

ax.set_aspect('equal', adjustable='box')
ax.axis('off')
plt.title(f"{str(gear).replace(chr(10), ' | ')} (Plot shows unscaled arrangement)")

plt.show()

print(f"\nExport complete. Check the '{output_dir}' directory for the .txt files.")
print(f"The exported profiles are scaled so the ring gear fits within a {TARGET_RING_DIAMETER_MM} mm diameter.")