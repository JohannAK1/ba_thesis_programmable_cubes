import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

class SinglePositionSaver2:
    def __init__(self, t_store, cube_types1, title):
        self.title = title
        self.t_store = t_store
        self.cube_types1 = cube_types1
        self.colors = {
            0: 'midnightblue',
            1: 'darkorange',
            2: 'snow',
            3: 'white',
            4: 'red',
            5: 'black',
            6: 'red',
            7: 'green'
        }

    def save_single_position(self, save_path, highlight_index, highlight_alpha=1.0, other_alpha=0.3):
        """
        Save a single position's voxel grid, with one cube highlighted by a different alpha.

        :param save_path: Path where the image will be saved
        :param highlight_index: The index of the position to be highlighted
        :param highlight_alpha: Alpha value for the highlighted cube
        :param other_alpha: Alpha value for the rest of the cubes
        """
        # Get the positions and types for the specific frame
        positions = self.t_store
        positions_array = np.array(positions)

        # Calculate the min and max values for positioning
        x_min, y_min, z_min = np.min(positions_array, axis=0)
        x_max, y_max, z_max = np.max(positions_array, axis=0)

        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = max(x_range, y_range, z_range)

        # Prepare grid for voxels
        voxels = np.zeros((max_range, max_range, max_range), dtype=bool)
        colors_grid = np.empty(voxels.shape, dtype=object)

        # Assign positions and colors to the voxel grid
        for idx, (pos, cube_type) in enumerate(zip(positions, self.cube_types1)):
            xi, yi, zi = pos[0] - x_min + 1, pos[1] - y_min + 1, pos[2] - z_min + 1
            voxels[xi, yi, zi] = True
            
            # Apply the alpha value depending on whether the position is highlighted or not
            if idx == highlight_index:
                alpha = highlight_alpha
            else:
                alpha = other_alpha
                
            colors_grid[xi, yi, zi] = mcolors.to_rgba(self.colors[cube_type], alpha=alpha)

        # Create a figure without the grid
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(voxels, facecolors=colors_grid, edgecolor='k')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(self.title)

        # Save the figure to the specified path
        plt.savefig(save_path)
        plt.close()


    def save_thesis_figure(self, save_path, highlight_index, highlight_alpha=1.0, other_alpha=0.5, dpi=300):
        """
        Save a single position's voxel grid, with one cube highlighted by a different alpha.

        :param save_path: Path where the image will be saved
        :param highlight_index: The index of the position to be highlighted
        :param highlight_alpha: Alpha value for the highlighted cube
        :param other_alpha: Alpha value for the rest of the cubes
        """
        positions = self.t_store
        positions_array = np.array(positions)

        x_min, y_min, z_min = np.min(positions_array, axis=0)
        x_max, y_max, z_max = np.max(positions_array, axis=0)

        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = max(x_range, y_range, z_range)

        voxels = np.zeros((max_range, max_range, max_range), dtype=bool)
        colors_grid = np.empty(voxels.shape, dtype=object)

        for idx, (pos, cube_type) in enumerate(zip(positions, self.cube_types1)):
            xi, yi, zi = pos[0] - x_min + 1, pos[1] - y_min + 1, pos[2] - z_min + 1
            voxels[xi, yi, zi] = True
            
            alpha = highlight_alpha if idx == highlight_index else other_alpha
            colors_grid[xi, yi, zi] = mcolors.to_rgba(self.colors[cube_type], alpha=alpha)

        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Only show the cubes, no labels or grid
        ax.voxels(voxels, facecolors=colors_grid, edgecolor='black', linewidth=0.5)

        # Remove axis, gridlines, and labels
        ax.set_axis_off()

        # Save the figure with high DPI
        plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()


    def save_fixed_view_figure(self, save_path,breakPoint, dpi=300):
        """
        Save a voxel grid with a fixed view from the front and no highlighted cubes.

        :param save_path: Path where the image will be saved
        :param dpi: DPI value for the saved image
        """
        positions = self.t_store
        positions_array = np.array(positions)

        x_min, y_min, z_min = np.min(positions_array, axis=0)
        x_max, y_max, z_max = np.max(positions_array, axis=0)

        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = max(x_range, y_range, z_range)

        voxels = np.zeros((max_range, max_range, max_range), dtype=bool)
        colors_grid = np.empty(voxels.shape, dtype=object)

        for idx, (pos, cube_type) in enumerate(zip(positions, self.cube_types1)):
            xi, yi, zi = pos[0] - x_min + 1, pos[1] - y_min + 1, pos[2] - z_min + 1
            voxels[xi, yi, zi] = True
            if idx >= breakPoint:
                #colors_grid[xi, yi, zi] = mcolors.to_rgba('red', alpha=0.5)
                colors_grid[xi, yi, zi] = mcolors.to_rgba(self.colors[cube_type], alpha=1)
            else:    
                #colors_grid[xi, yi, zi] = mcolors.to_rgba('green', alpha=1)
                colors_grid[xi, yi, zi] = mcolors.to_rgba(self.colors[cube_type], alpha=.2)


        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')

        # Render the cubes without highlighting and without changing transparency
        ax.voxels(voxels, facecolors=colors_grid, edgecolor="black", linewidth=0.5)

        # Set fixed view from the front
        #ax.view_init(elev=90, azim=-90)

        # Remove axis, gridlines, and labels
        ax.set_axis_off()

        # Save the figure with high DPI
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
        plt.close()


    