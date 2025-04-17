import matplotlib.pyplot as plt
import numpy as np
import os
import math # For trigonometric functions

# Import the classes for single-stage planetary gears
from pygeartrain.planetary import Planetary, PlanetaryGeometry

# --- User Defined Parameters ---
TARGET_RING_DIAMETER_MM = 70.0   # Desired outer diameter for the ring gear in mm
GEAR_THICKNESS_MM = 10.0       # Total face width of the gear (Z-axis)
HELIX_ANGLE_DEGREES = 20.0     # Helix angle for one half of the herringbone/helix
GEAR_TYPE = 'herringbone'        # Choose 'helix' or 'herringbone'
CARRIER_PATH_POINTS = 200      # Number of points for the carrier path circle
CLOSE_POINT_TOLERANCE = 1e-7     # Tolerance for removing duplicate/close points
SMALL_RADIUS_TOLERANCE = 1e-9  # Avoid division by zero for points near origin

# --- Parameters derived from the "Blue" Stage (Stage 2) ---
R_teeth = 30
P_teeth = 12
S_teeth = 6
N_planets = 3
b_profile = 0.5

# --- Define Single-Stage Planetary Kinematics ---
kinematics = Planetary('s', 'c', 'r') # Sun input, Carrier output, Ring fixed

# --- Define Geometry ---
G = (R_teeth, P_teeth, S_teeth)

# --- Create the Gear Geometry Object ---
# This object holds the unscaled geometry and kinematic info needed for animation
gear = PlanetaryGeometry.create(
    kinematics=kinematics,
    G=G,
    N=N_planets,
    b=b_profile
)

# --- Print Gear Information ---
print("Generated Single-Stage Planetary Gear Configuration:")
print(gear)
print(f"\nTarget Ring Diameter: {TARGET_RING_DIAMETER_MM:.2f} mm")
print(f"Gear Thickness: {GEAR_THICKNESS_MM:.2f} mm")
print(f"Helix Angle: {HELIX_ANGLE_DEGREES:.2f} degrees")
print(f"Gear Type: {GEAR_TYPE}")


# --- Get Base Profiles (Unscaled) ---
base_ring_profile, base_planet_profile, base_sun_profile, _ = gear.generate_profiles

# --- Calculate Scaling Factor ---
unscaled_ring_vertices = base_ring_profile.vertices
radii = np.linalg.norm(unscaled_ring_vertices, axis=1)
max_radius_unscaled = np.max(radii)
target_radius = TARGET_RING_DIAMETER_MM / 2.0
if max_radius_unscaled <= 1e-9:
    print("Warning: Unscaled ring gear has zero radius. Cannot calculate scale factor.")
    scale_factor = 1.0
else:
    scale_factor = target_radius / max_radius_unscaled
print(f"Calculated Scale Factor: {scale_factor:.6f}")

# --- Calculate Scaled Planet Center Radius ---
scaled_planet_center_radius = 1.0 * scale_factor
print(f"Scaled Planet Center Radius (Carrier Path Radius): {scaled_planet_center_radius:.4f} mm")


# --- Prepare Data for SolidWorks Export ---
output_dir = f"output_{GEAR_TYPE}" # Directory name reflects type
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Output directory already exists: {output_dir}")

# Convert base helix angle to radians
helix_angle_rad = math.radians(HELIX_ANGLE_DEGREES)
# Use tangent for calculations
base_tan_helix_angle = math.tan(helix_angle_rad)

# --- Function definitions (apply_twist, save_curve_to_file, save_gear_profiles) ---
# ... (insert the exact functions from the previous herringbone/helix answer here) ...
# --- Function to apply twist and return 3D points (Updated) ---
def apply_twist(xy_points, z_offset, tan_helix_for_gear, is_herringbone):
    """Applies helix or herringbone twist to 2D points for a given Z offset."""
    twisted_points_3d = []
    z_for_twist_calc = z_offset
    if is_herringbone:
         z_for_twist_calc = abs(z_offset)
    if abs(z_offset) < SMALL_RADIUS_TOLERANCE:
         for x, y in xy_points:
            twisted_points_3d.append([x, y, z_offset])
         return np.array(twisted_points_3d)
    for x, y in xy_points:
        radius = math.sqrt(x**2 + y**2)
        if radius < SMALL_RADIUS_TOLERANCE:
            x_new, y_new = x, y
        else:
            twist_angle = (z_for_twist_calc * tan_helix_for_gear) / radius
            cos_twist = math.cos(twist_angle)
            sin_twist = math.sin(twist_angle)
            x_new = x * cos_twist - y * sin_twist
            y_new = x * sin_twist + y * cos_twist
        twisted_points_3d.append([x_new, y_new, z_offset])
    return np.array(twisted_points_3d)

# --- Function to filter, ensure closure, and save ---
def save_curve_to_file(points_3d, filepath):
    """Saves 3D points to a text file for SolidWorks."""
    if points_3d is None or len(points_3d) < 3:
        print(f"Warning: Not enough points to save file {filepath}")
        return
    first_point = points_3d[0, :2]
    last_point = points_3d[-1, :2]
    effective_tolerance = CLOSE_POINT_TOLERANCE * max(1.0, np.linalg.norm(first_point))
    if np.linalg.norm(last_point - first_point) > effective_tolerance:
        print(f"    -> Forcing closure for {os.path.basename(filepath)}.")
        points_3d = np.vstack((points_3d, points_3d[0]))
    np.savetxt(filepath, points_3d, fmt='%.8f', delimiter=' ')
    print(f"Exported curve ({len(points_3d)} points) to: {filepath}")

# --- Function to process and save profiles for one gear (Updated) ---
def save_gear_profiles(profile, gear_name, tooth_count, scale_factor, thickness, base_tan_helix, gear_type):
    """Generates and saves the three curves (z=0, z=+t/2, z=-t/2) for a gear,
       handling helix/herringbone and meshing direction."""
    if profile is None or len(profile.vertices) < 3:
        print(f"Warning: Not enough base vertices for {gear_name}. Skipping export.")
        return
    print(f"\nProcessing {gear_name} ({tooth_count} teeth) as {gear_type}...")
    if gear_name == 'sun':
        tan_helix_for_gear = base_tan_helix
        print(f"  - Using base helix direction (tan={tan_helix_for_gear:.4f})")
    else: # planet or ring
        tan_helix_for_gear = -base_tan_helix
        print(f"  - Using opposite helix direction (tan={tan_helix_for_gear:.4f})")
    is_herringbone_flag = (gear_type.lower() == 'herringbone')
    vertices_2d_scaled = profile.vertices * scale_factor
    filtered_points_2d = [vertices_2d_scaled[0]]
    for i in range(len(vertices_2d_scaled) - 1):
        point_current = filtered_points_2d[-1]
        point_next = vertices_2d_scaled[i+1]
        distance = np.linalg.norm(point_next - point_current)
        if distance > CLOSE_POINT_TOLERANCE * scale_factor:
            filtered_points_2d.append(point_next)
    filtered_points_2d = np.array(filtered_points_2d)
    print(f"  Base points: {len(profile.vertices)}, Scaled points: {len(vertices_2d_scaled)}, Filtered 2D points: {len(filtered_points_2d)}")
    if len(filtered_points_2d) < 3:
         print(f"Warning: Not enough vertices after filtering for {gear_name}. Skipping export.")
         return
    z0 = 0.0
    z_pos = thickness / 2.0
    z_neg = -thickness / 2.0
    points_z0 = apply_twist(filtered_points_2d, z0, tan_helix_for_gear, is_herringbone_flag)
    points_z_pos = apply_twist(filtered_points_2d, z_pos, tan_helix_for_gear, is_herringbone_flag)
    points_z_neg = apply_twist(filtered_points_2d, z_neg, tan_helix_for_gear, is_herringbone_flag)
    base_filename = f"{gear_name}_{tooth_count}"
    filepath_z0 = os.path.join(output_dir, f"{base_filename}_z0.txt")
    filepath_z_pos = os.path.join(output_dir, f"{base_filename}_z_pos.txt")
    filepath_z_neg = os.path.join(output_dir, f"{base_filename}_z_neg.txt")
    save_curve_to_file(points_z0, filepath_z0)
    save_curve_to_file(points_z_pos, filepath_z_pos)
    save_curve_to_file(points_z_neg, filepath_z_neg)

# --- Save Gear Profiles ---
print(f"\nExporting {GEAR_TYPE} gear profiles...")
save_gear_profiles(base_ring_profile, "ring", R_teeth, scale_factor, GEAR_THICKNESS_MM, base_tan_helix_angle, GEAR_TYPE)
save_gear_profiles(base_planet_profile, "planet", P_teeth, scale_factor, GEAR_THICKNESS_MM, base_tan_helix_angle, GEAR_TYPE)
save_gear_profiles(base_sun_profile, "sun", S_teeth, scale_factor, GEAR_THICKNESS_MM, base_tan_helix_angle, GEAR_TYPE)


# --- Generate and Save Carrier Path (Planet Center Circle) ---
print("\nGenerating and exporting carrier path (planet center circle)...")
angles = np.linspace(0, 2 * np.pi, CARRIER_PATH_POINTS, endpoint=True)
carrier_x = scaled_planet_center_radius * np.cos(angles)
carrier_y = scaled_planet_center_radius * np.sin(angles)
carrier_points_3d = np.column_stack((carrier_x, carrier_y, np.zeros_like(carrier_x)))
carrier_filename = "carrier_path.txt"
carrier_filepath = os.path.join(output_dir, carrier_filename)
np.savetxt(carrier_filepath, carrier_points_3d, fmt='%.8f', delimiter=' ')
print(f"Exported carrier path ({len(carrier_points_3d)} points) to: {carrier_filepath}")


# --- Animate the Gearbox (Using Unscaled Profiles) ---
# This replaces the static plot section
print("\nStarting animation (displays unscaled gear motion)...")
# Note: The gear object 'gear' contains the unscaled geometry and kinematics
# The animate() method uses the internal plot() method which arranges these.
try:
    # gear.animate(scale=0.02) # You can adjust scale for speed if needed
    gear.animate() # Use default scaling/speed
    print("Animation window closed by user.")
except Exception as e:
    print(f"Animation failed or was interrupted: {e}")
    print("If animation window didn't appear, check your matplotlib backend configuration.")

print(f"\n{GEAR_TYPE.capitalize()} export complete. Check the '{output_dir}' directory for scaled/twisted profiles.")