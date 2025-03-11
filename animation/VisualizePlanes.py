import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from LayerFreeCube import LayerFreeCube
# Define the dimensions for the space
x_dim = 4  # Length along x-axis
y_dim = 5  # Length along y-axis
z_dim = 8  # Length along z-axis

# Initialize an empty array to store the coordinates
coordinates = []

# Generate the coordinates
for x in range(x_dim + 1):
    for y in range(y_dim + 1):
        for z in range(z_dim + 1):
            coordinates.append([x, y, z])

def create_marked_array(dimensions, special_coord):
    """
    Creates an array with the same number of indexes as the generated coordinates.
    All values are 1 with alpha 0.3, except for the special coordinate, which is marked as 2 with alpha 1.0.
    Additionally, marks the x, y, and z planes of the special coordinate with different numbers and alpha 0.7.

    :param dimensions: Tuple containing the dimensions (x_dim, y_dim, z_dim).
    :param special_coord: List specifying the coordinate to mark as 2.
    :return: List of tuples containing the value and alpha for each coordinate.
    """
    total_elements = (dimensions[0] + 1) * (dimensions[1] + 1) * (dimensions[2] + 1)
    array = [(1, 0.01)] * total_elements

    # Calculate the index of the special coordinate
    index = (special_coord[0] * (dimensions[1] + 1) * (dimensions[2] + 1)) + \
            (special_coord[1] * (dimensions[2] + 1)) + special_coord[2]
    array[index] = (2, 1.0)
    cIndex = index

    alpha_Plane = 1

    # Mark the x-plane
    for y in range(dimensions[1] + 1):
        for z in range(dimensions[2] + 1):
            plane_index = (special_coord[0] * (dimensions[1] + 1) * (dimensions[2] + 1)) + \
                          (y * (dimensions[2] + 1)) + z
            if plane_index != index:
                array[plane_index] = (3, alpha_Plane)

    # Mark the y-plane
    for x in range(dimensions[0] + 1):
        for z in range(dimensions[2] + 1):
            plane_index = (x * (dimensions[1] + 1) * (dimensions[2] + 1)) + \
                          (special_coord[1] * (dimensions[2] + 1)) + z
            if plane_index != index:
                array[plane_index] = (4, alpha_Plane)

    # Mark the z-plane
    for x in range(dimensions[0] + 1):
        for y in range(dimensions[1] + 1):
            plane_index = (x * (dimensions[1] + 1) * (dimensions[2] + 1)) + \
                          (y * (dimensions[2] + 1)) + special_coord[2]
            if plane_index != index:
                array[plane_index] = (5, alpha_Plane)

    return array,cIndex

class SinglePositionSaver:
    def __init__(self, t_store, cube_types1, title):
        self.title = title
        self.t_store = t_store
        self.cube_types1 = cube_types1
        self.colors = {
            1: 'white',
            2: 'red',
            3: 'green',
            4: 'blue',
            5: 'yellow',
        }

    def save_single_position(self, save_path, highlight_index, highlight_alpha=1.0, other_alpha=0.3):
        """
        Save a single position's voxel grid, ensuring all cubes are visible with uniform scaling.

        :param save_path: Path where the image will be saved
        :param highlight_index: The index of the position to be highlighted
        :param highlight_alpha: Alpha value for the highlighted cube
        :param other_alpha: Alpha value for the rest of the cubes
        """
        # Get the positions and types for the specific frame
        positions = self.t_store
        cube_types = self.cube_types1

        # Calculate the min and max values for positioning
        positions_array = np.array(positions)
        x_min, y_min, z_min = np.min(positions_array, axis=0)
        x_max, y_max, z_max = np.max(positions_array, axis=0)

        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = max(x_range, y_range, z_range)

        # Create a figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Draw each cube manually
        for idx, (pos, cube_type) in enumerate(zip(positions, cube_types)):
            x, y, z = pos[0] - x_min + 1, pos[1] - y_min + 1, pos[2] - z_min + 1
            value, alpha = cube_type
            #alpha = highlight_alpha if idx == highlight_index else other_alpha
            color = mcolors.to_rgba(self.colors[value], alpha=alpha)

            # Draw a transparent cube at the specified position
            ax.bar3d(
                x - 0.5, y - 0.5, z - 0.5,  # Center of the cube
                1, 1, 1,  # Uniform width, depth, height
                shade=False,
                color=color,
                edgecolor='k'  # Add edges for visibility
            )

        # Remove the grid, labels, and title
        ax.set_axis_off()

        # Equalize scaling to ensure cubes look uniform
        ax.set_box_aspect([x_range, y_range, z_range])  # Ensure equal scaling across all axes

        # Adjust view angle for better visibility
        ax.view_init(elev=25, azim=30)

        # Save the figure to the specified path
        plt.savefig(save_path, dpi=300)
        plt.close()


    def save_single_color(self, save_path, color_value, highlight_alpha=1.0, other_alpha=0.0):
        """
        Save a visualization where all cubes are rendered, but only the cubes with the specified color value are visible.

        :param save_path: Path where the image will be saved
        :param color_value: The color value of the cubes to be shown
        :param highlight_alpha: Alpha value for the visible cubes
        :param other_alpha: Alpha value for the hidden cubes
        """
        # Get the positions and types for the specific frame
        positions = self.t_store
        cube_types = self.cube_types1

        # Calculate the min and max values for positioning
        positions_array = np.array(positions)
        x_min, y_min, z_min = np.min(positions_array, axis=0)
        x_max, y_max, z_max = np.max(positions_array, axis=0)

        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3

        # Create a figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Render all cubes but adjust their transparency based on the color value
        for pos, cube_type in zip(positions, cube_types):
            value, alpha = cube_type
            x, y, z = pos[0] - x_min + 1, pos[1] - y_min + 1, pos[2] - z_min + 1
            cube_alpha = highlight_alpha if value == color_value else other_alpha
            color = mcolors.to_rgba(self.colors[value], alpha=cube_alpha)

            # Draw the cube
            ax.bar3d(
                x - 0.5, y - 0.5, z - 0.5,  # Center of the cube
                1, 1, 1,  # Uniform width, depth, height
                shade=False,
                color=color,
                edgecolor='k' if cube_alpha > 0 else None  # Outline only visible cubes
            )

        # Remove the grid, labels, and title
        ax.set_axis_off()

        # Equalize scaling to ensure cubes look uniform
        ax.set_box_aspect([x_range, y_range, z_range])  # Consistent aspect ratio

        # Adjust view angle to match the first method
        ax.view_init(elev=30, azim=45)

        # Save the figure to the specified path
        plt.savefig(save_path, dpi=300)
        plt.close()


    def save_single_color_with_special(self, save_path, color_value, special_coordinate, highlight_alpha=1.0, other_alpha=0.01, special_alpha=1.0):
        """
        Save a visualization where all cubes are rendered, but only the cubes with the specified color value
        and the special coordinate are visible.

        :param save_path: Path where the image will be saved
        :param color_value: The color value of the cubes to be shown
        :param special_coordinate: The (x, y, z) position of the special cube
        :param highlight_alpha: Alpha value for the visible cubes
        :param other_alpha: Alpha value for the hidden cubes
        :param special_alpha: Alpha value for the special cube
        """
        # Get the positions and types for the specific frame
        positions = self.t_store
        cube_types = self.cube_types1

        # Calculate the min and max values for positioning
        positions_array = np.array(positions)
        x_min, y_min, z_min = np.min(positions_array, axis=0)
        x_max, y_max, z_max = np.max(positions_array, axis=0)

        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3

        # Create a figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Render all cubes but adjust their transparency based on the color value and special coordinate
        for pos, cube_type in zip(positions, cube_types):
            value, alpha = cube_type
            x, y, z = pos[0] - x_min + 1, pos[1] - y_min + 1, pos[2] - z_min + 1
            is_special = np.array_equal(pos, special_coordinate)
            cube_alpha = (
                special_alpha if is_special else 
                highlight_alpha if value == color_value else 
                other_alpha
            )
            color = mcolors.to_rgba(self.colors[value], alpha=cube_alpha)
            eColor = mcolors.to_rgba('k', alpha=0.05)
            # Draw the cube
            ax.bar3d(
                x - 0.5, y - 0.5, z - 0.5,  # Center of the cube
                1, 1, 1,  # Uniform width, depth, height
                shade=False,
                color=color,
                edgecolor='k' if cube_alpha > 0.5 else eColor  # Outline only visible cubes
            )

        # Remove the grid, labels, and title
        ax.set_axis_off()

        # Equalize scaling to ensure cubes look uniform
        ax.set_box_aspect([x_range, y_range, z_range])  # Consistent aspect ratio

        # Adjust view angle to match the first method
        ax.view_init(elev=25, azim=30)

        #plt.show()
        # Save the figure to the specified path
        plt.savefig(save_path, dpi=300)
        plt.close()








# Example usage
special_coordinate = [2, 3, 4]
marked_array,idx = create_marked_array((x_dim, y_dim, z_dim), special_coordinate)

configs = np.array(coordinates)
print(configs)
print(configs[idx])
LFC = LayerFreeCube(configs,idx,2)
#LFC.freeCube()


print(idx)
#print(LFC.freeCube())
moves = [(265, 0), (256, 1), (256, 1), (247, 1), (247, 1), (265, 0), (265, 0), (211, 0), (202, 1), (202, 1), (193, 1), (211, 0), (157, 0), (148, 0)]

pusPOS = LFC.moves2Position(moves)


saver = SinglePositionSaver(pusPOS, marked_array, "Plane Vis")
saver.save_single_position("voxel_grid.png", highlight_index=0)
saver.save_single_color("one_color_grid",5,1)
saver.save_single_color_with_special("output_color5_with_special.png", color_value=5, special_coordinate=special_coordinate)
