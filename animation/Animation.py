import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
from framework.programmable_cubes_UDP import ProgrammableCubes

class CubeAnimation:
    def __init__(self, moves, initConfig, cube_types1, num_steps, interval,name):
        self.t_store = self.createStorage(moves, initConfig)
        self.cube_types1 = cube_types1
        self.num_steps = num_steps
        self.interval = interval
        self.name = name

        # Define colors for different cube types
        self.colors = {
            0: 'midnightblue',
            1: 'darkorange',
            2: 'snow',
            3: 'white',
            4: 'pink',
            5: 'black',
            6: 'red',
            7: 'green'
        }

        self.fig = plt.figure(figsize=(20, 20))
        self.ax = self.fig.add_subplot(111, projection='3d')

    def update(self, frame):
        positions = self.t_store[frame]
        positions_array = np.array(positions)

        x_min, y_min, z_min = np.min(positions_array, axis=0)
        x_max, y_max, z_max = np.max(positions_array, axis=0)

        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = max(x_range, y_range, z_range)

        x, y, z = np.indices((max_range, max_range, max_range))

        voxels = np.zeros((max_range, max_range, max_range), dtype=bool)
        colors_grid = np.empty(voxels.shape, dtype=object)

        for pos, cube_type in zip(positions, self.cube_types1):
            xi, yi, zi = pos[0] - x_min + 1, pos[1] - y_min + 1, pos[2] - z_min + 1
            voxels[xi, yi, zi] = True
            colors_grid[xi, yi, zi] = mcolors.to_rgba(self.colors[cube_type], alpha=0.9)

        self.ax.clear()
        self.ax.voxels(voxels, facecolors=colors_grid, edgecolor='k')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title(f'Frame {frame + 1}/{len(self.t_store)}')

    def init(self):
        return []

    def make_animation(self):
        # Create the animation
        ani = FuncAnimation(self.fig, self.update, frames=np.arange(0, len(self.t_store), self.num_steps),
                            init_func=self.init, interval=self.interval, blit=False)

        ani.save('images/' + self.name + '.gif', writer='pillow')

    def show_configuration(self, frame):
        # Display a single frame's configuration without saving
        self.update(frame)
        plt.show()

    def createStorage(self, moves, config):
        cubes = ProgrammableCubes(np.copy(config))
        storage = []

        for cID, move in moves:
            done = cubes.apply_single_update_step(cID, move)
            storage.append(np.copy(cubes.cube_position))
            if not done:
                print("Failed to apply move, storage could not be created")
                return storage
        return storage