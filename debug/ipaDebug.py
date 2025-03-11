import os
import json
from datetime import datetime
import numpy as np
from framework.programmable_cubes_UDP import ProgrammableCubes
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.animation import FuncAnimation


def saveErrorConfig(config, cubeID, gPos, errorMethod):
    """
    Saves the configuration, cubeID, gPos and errorMethod as JSON.

    Parameters:
        config: The configuration (if it's a numpy array, it is converted to a list)
        cubeID: The cube identifier
        gPos: The gPos value
        errorMethod: A string describing the error method

    Returns:
        The path to the saved JSON file.
    """
    # Convert numpy array to list if needed
    if isinstance(config, np.ndarray):
        config = config.tolist()
    
    if isinstance(gPos, np.ndarray):
        gPos = gPos.tolist()

    # Define the target directory (debug/debugConfigs relative to this file)
    current_dir = os.path.dirname(__file__)
    target_dir = os.path.join(current_dir, "debugConfigs")
    os.makedirs(target_dir, exist_ok=True)
    
    # Build a filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"errorConfig_{timestamp}.json"
    file_path = os.path.join(target_dir, filename)
    
    # Build the data dictionary to save
    data = {
        "configuration": config,
        "cubeID": cubeID,
        "gPos": gPos,
        "errorMethod": errorMethod
    }
    
    # Write data to the JSON file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Configuration error saved to {file_path}")
    return file_path

def loadErrorConfig(file_path):
    """
    Loads the error configuration from the specified JSON file.

    Parameters:
        file_path: The path to the JSON file containing error configuration.

    Returns:
        The loaded data as a dictionary.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def createStorage(moves, config):
    cubes = ProgrammableCubes(np.copy(config))
    storage = []

    for cID, move in moves:
        done = cubes.apply_single_update_step(cID, move)
        storage.append(np.copy(cubes.cube_position))
        if not done:
            print("Layer free Cube: Move could not be made")
            return storage
    return storage


def getNotPossibleMove(moves,config): 
    cubes = ProgrammableCubes(np.copy(config))
    configDict = {}
    oppositeMoves = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}
    for cID, move in moves: 
        done = cubes.apply_single_update_step(cID, move)
        if not done: 
            return (cID, configDict[(cID,oppositeMoves[move])])
        configDict[(cID,move)] = np.copy(cubes.cube_position)
    return None

def visualizeMoves(moves, config, cube, gPos):
    """
    Visualizes the moves with an animation. All cubes except the one with index "cube"
    are drawn in gray. Additionally, the gPos position is added in each frame as a red cube.
    
    Parameters:
        moves: List of (cubeID, move) pairs.
        config: The initial configuration.
        cube: The index of the cube to highlight (drawn in red).
        gPos: The goal position to add in every frame (drawn in red).
    """
    # Create the storage of positions from moves
    t_store = createStorage(moves, config)
    
    # Set up the figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    def update(frame):
        positions = t_store[frame]
        positions = np.array(positions)
        
        # Include gPos in the bounds calculation
        all_positions = np.vstack([positions, np.atleast_1d(gPos)])
        x_min, y_min, z_min = np.min(all_positions, axis=0)
        x_max, y_max, z_max = np.max(all_positions, axis=0)
        
        # Add a margin
        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = int(max(x_range, y_range, z_range))
        
        # Initialize voxel grid and color grid
        voxels = np.zeros((max_range, max_range, max_range), dtype=bool)
        colors_grid = np.empty(voxels.shape, dtype=object)
        
        # Plot each cube from the storage; highlight "cube" in green, others gray.
        for idx, pos in enumerate(positions):
            xi = int(pos[0] - x_min + 1)
            yi = int(pos[1] - y_min + 1)
            zi = int(pos[2] - z_min + 1)
            voxels[xi, yi, zi] = True
            if idx == cube:
                colors_grid[xi, yi, zi] = mcolors.to_rgba('green', alpha=1)
            else:
                colors_grid[xi, yi, zi] = mcolors.to_rgba('gray', alpha=0.3)
                
        # Add the goal position (gPos) as a red cube.
        gpos_arr = np.array(gPos)
        xi = int(gpos_arr[0] - x_min + 1)
        yi = int(gpos_arr[1] - y_min + 1)
        zi = int(gpos_arr[2] - z_min + 1)
        voxels[xi, yi, zi] = True
        colors_grid[xi, yi, zi] = mcolors.to_rgba('red', alpha=1)
        
        ax.clear()
        # Set edgecolor to a transparent value so edges are not drawn with the same alpha.
        ax.voxels(voxels, facecolors=colors_grid, edgecolor=(0, 0, 0, 0))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Frame {frame + 1}/{len(t_store)}')
    
    ani = FuncAnimation(fig, update, frames=np.arange(0, len(t_store)), interval=500, blit=False)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "visualizeMoves.gif")
    ani.save(output_file, writer="pillow")
    print(f"Animation saved to {output_file}")
    plt.show()

def visualizeConfig(config, cube, gPos):
    """
    Visualizes the moves with an animation. All cubes except the one with index "cube"
    are drawn in gray. Additionally, the gPos position is added in each frame as a red cube.
    
    Parameters:
        moves: List of (cubeID, move) pairs.
        config: The initial configuration.
        cube: The index of the cube to highlight (drawn in red).
        gPos: The goal position to add in every frame (drawn in red).
    """
    # Create the storage of positions from moves
    t_store = [config]
    
    # Set up the figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    def update(frame):
        positions = t_store[frame]
        positions = np.array(positions)
        
        # Include gPos in the bounds calculation
        all_positions = np.vstack([positions, np.atleast_1d(gPos)])
        x_min, y_min, z_min = np.min(all_positions, axis=0)
        x_max, y_max, z_max = np.max(all_positions, axis=0)
        
        # Add a margin
        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = int(max(x_range, y_range, z_range))
        
        # Initialize voxel grid and color grid
        voxels = np.zeros((max_range, max_range, max_range), dtype=bool)
        colors_grid = np.empty(voxels.shape, dtype=object)
        
        # Plot each cube from the storage; highlight "cube" in green, others gray.
        for idx, pos in enumerate(positions):
            xi = int(pos[0] - x_min + 1)
            yi = int(pos[1] - y_min + 1)
            zi = int(pos[2] - z_min + 1)
            voxels[xi, yi, zi] = True
            if idx == cube:
                colors_grid[xi, yi, zi] = mcolors.to_rgba('green', alpha=1)
            else:
                colors_grid[xi, yi, zi] = mcolors.to_rgba('gray', alpha=0.6)
                
        # Add the goal position (gPos) as a red cube.
        gpos_arr = np.array(gPos)
        xi = int(gpos_arr[0] - x_min + 1)
        yi = int(gpos_arr[1] - y_min + 1)
        zi = int(gpos_arr[2] - z_min + 1)
        voxels[xi, yi, zi] = True
        colors_grid[xi, yi, zi] = mcolors.to_rgba('red', alpha=1)
        
        ax.clear()
        # Set edgecolor to a transparent value so edges are not drawn with the same alpha.
        ax.voxels(voxels, facecolors=colors_grid, edgecolor=(0, 0, 0, 0))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Frame {frame + 1}/{len(t_store)}')
    
    ani = FuncAnimation(fig, update, frames=np.arange(0, len(t_store)), interval=500, blit=False)
    #output_dir = os.path.join(os.path.dirname(__file__), "..", "images")
    #os.makedirs(output_dir, exist_ok=True)
    #output_file = os.path.join(output_dir, "visualizeMoves.gif")
    #ani.save(output_file, writer="pillow")
    #print(f"Animation saved to {output_file}")
    plt.show()


def visualizeMoves2(moves, config, cube, gPos):
    """
    Visualizes the moves with an animation. All cubes except the one with index "cube"
    are drawn in gray. Additionally, the gPos position is added in each frame as a red cube.
    
    If getNotPossibleMove returns a non-None value, then the resulting configuration is appended 
    to the end of the storage and the error cube is highlighted in yellow for that frame.
    
    Parameters:
        moves: List of (cubeID, move) pairs.
        config: The initial configuration.
        cube: The index of the cube to highlight normally (drawn in green).
        gPos: The goal position to add in every frame (drawn in red).
    """
    # Create the storage of positions from moves
    t_store = createStorage(moves, config)
    errorTuple = getNotPossibleMove(moves, config)
    errorCube = None
    if errorTuple is not None:
        errorCube = errorTuple[0]
        t_store.append(errorTuple[1])
    
    # Set up the figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    def update(frame):
        positions = t_store[frame]
        positions = np.array(positions)
        
        # Include gPos in the bounds calculation
        all_positions = np.vstack([positions, np.atleast_1d(gPos)])
        x_min, y_min, z_min = np.min(all_positions, axis=0)
        x_max, y_max, z_max = np.max(all_positions, axis=0)
        
        # Add a margin
        x_range = x_max - x_min + 3
        y_range = y_max - y_min + 3
        z_range = z_max - z_min + 3
        max_range = int(max(x_range, y_range, z_range))
        
        # Initialize voxel grid and color grid
        voxels = np.zeros((max_range, max_range, max_range), dtype=bool)
        colors_grid = np.empty(voxels.shape, dtype=object)
        
        # For each cube in the configuration: 
        #   normally highlight the designated cube (green) and all others gray,
        #   but if this frame is the error configuration (last frame) then highlight the error cube in yellow.
        for idx, pos in enumerate(positions):
            xi = int(pos[0] - x_min + 1)
            yi = int(pos[1] - y_min + 1)
            zi = int(pos[2] - z_min + 1)
            voxels[xi, yi, zi] = True
            # If this is the last frame and there is an error, highlight errorCube in yellow.
            if errorCube is not None:
                if idx == errorCube:
                    colors_grid[xi, yi, zi] = mcolors.to_rgba('yellow', alpha=1)
                elif idx == cube:
                    colors_grid[xi, yi, zi] = mcolors.to_rgba('green', alpha=1)
                else:
                    colors_grid[xi, yi, zi] = mcolors.to_rgba('gray', alpha=0.3)
            else:
                if idx == cube:
                    colors_grid[xi, yi, zi] = mcolors.to_rgba('green', alpha=1)
                else:
                    colors_grid[xi, yi, zi] = mcolors.to_rgba('gray', alpha=0.3)
                
        # Add the goal position (gPos) as a red cube.
        gpos_arr = np.array(gPos)
        xi = int(gpos_arr[0] - x_min + 1)
        yi = int(gpos_arr[1] - y_min + 1)
        zi = int(gpos_arr[2] - z_min + 1)
        voxels[xi, yi, zi] = True
        colors_grid[xi, yi, zi] = mcolors.to_rgba('red', alpha=1)
        
        ax.clear()
        # Set edgecolor to transparent so that edges don't inherit the same alpha.
        ax.voxels(voxels, facecolors=colors_grid, edgecolor=(0, 0, 0, 0))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Frame {frame + 1}/{len(t_store)}')
    
    ani = FuncAnimation(fig, update, frames=np.arange(0, len(t_store)), interval=500, blit=False)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "visualizeMoves.gif")
    ani.save(output_file, writer="pillow")
    print(f"Animation saved to {output_file}")
    plt.show()