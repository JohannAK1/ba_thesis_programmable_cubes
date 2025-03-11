import numpy as np
import queue
from framework.programmable_cubes_UDP import ProgrammableCubes

class LayerCubes: 
    def __init__(self, configuration,cubeID):
        self.position = np.copy(configuration)
        self.cubeID = cubeID
        
        self.layer2xyz= {
            0: [1,2],
            1: [0,2],
            2: [0,1]
        }

    def getLayerCubes(self,layer): 
        cubeLayerCoord = self.position[self.cubeID][layer]
        return [i for i, coord in enumerate(self.position) if coord[layer] == cubeLayerCoord]

    def getCubesNeededSets(self):
        """
        Divide cubes into quarters based on their positions in the layer and return all subsets sorted by size, smallest first.
        """
        allLayerQuarters = {}
        for layer in range(3):
            # Identify the axes for the layer
            axes = self.layer2xyz[layer]
            axis_1, axis_2 = axes[0], axes[1]

            # Divide cubes into four quarters based on their positions in the layer
            quarters = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
            layerCoord = self.position[self.cubeID][layer]
            for i in self.getLayerCubes(layer):
                coord = self.position[i]
                if coord[layer] == layerCoord:  # Ensure the cube is in the current layer
                    x, y = coord[axis_1], coord[axis_2]
                    cube_x = self.position[self.cubeID][axis_1]
                    cube_y = self.position[self.cubeID][axis_2]

                    # Assign cubes to quarters
                    if x >= cube_x and y >= cube_y:
                        quarters["Q1"].append(i)  # Top-right quarter
                    if x <= cube_x and y >= cube_y:
                        quarters["Q2"].append(i)  # Bottom-right quarter
                    if x >= cube_x and y <= cube_y:
                        quarters["Q3"].append(i)  # Top-left quarter
                    if x <= cube_x and y <= cube_y:
                        quarters["Q4"].append(i)  # Bottom-left quarter
            
            # Create a list of tuples (quarter_name, cube_list) and sort by the length of cube_list
            sorted_quarters = sorted(quarters.items(), key=lambda q: len(q[1]))

            allLayerQuarters[layer] = [(q, sorted(cubes)) for q, cubes in sorted_quarters]

        sorted_allLayers = sorted(allLayerQuarters.items(), key=lambda q: len(q[1]))
            # Return the sorted lists of cube IDs
        

        # Flatten the list and filter out sublists with only one element
        flattened_list = [(item[0], sublist[1], sublist[0]) for item in sorted_allLayers for sublist in item[1] if len(sublist[1]) > 1]

        # Sort by the length of the sublists
        sorted_flattened_list = sorted(flattened_list, key=lambda x: len(x[1]))
        
        #print(sorted_flattened_list)
        return sorted_flattened_list

    def getCubesNeededSetsDependend(self):
        """
        Divide cubes into quarters based on their positions in the layer and return all subsets sorted by size, smallest first.
        Filters out quarters that have dependent cubes.
        """
        allLayerQuarters = {}
        for layer in range(3):
            # Identify the axes for the layer
            axes = self.layer2xyz[layer]
            axis_1, axis_2 = axes[0], axes[1]

            # Divide cubes into four quarters based on their positions in the layer
            quarters = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
            layerCoord = self.position[self.cubeID][layer]
            for i in self.getLayerCubes(layer):
                coord = self.position[i]
                if coord[layer] == layerCoord:  # Ensure the cube is in the current layer
                    x, y = coord[axis_1], coord[axis_2]
                    cube_x = self.position[self.cubeID][axis_1]
                    cube_y = self.position[self.cubeID][axis_2]

                    # Assign cubes to quarters
                    if x >= cube_x and y >= cube_y:
                        quarters["Q1"].append(i)  # Top-right quarter
                    if x <= cube_x and y >= cube_y:
                        quarters["Q2"].append(i)  # Bottom-right quarter
                    if x >= cube_x and y <= cube_y:
                        quarters["Q3"].append(i)  # Top-left quarter
                    if x <= cube_x and y <= cube_y:
                        quarters["Q4"].append(i)  # Bottom-left quarter

            # Filter out quarters with dependent cubes and create sorted list
            filtered_quarters = []
            for quarter_name, cube_list in quarters.items():
                if len(cube_list) > 1 and not self.haveDependentCubes(cube_list):
                    filtered_quarters.append((quarter_name, cube_list))
            
            # Sort the filtered quarters by length
            sorted_quarters = sorted(filtered_quarters, key=lambda q: len(q[1]))
            allLayerQuarters[layer] = [(q, sorted(cubes)) for q, cubes in sorted_quarters]

        sorted_allLayers = sorted(allLayerQuarters.items(), key=lambda q: len(q[1]))

        # Flatten the list (no need to filter sublists with one element as it's done above)
        flattened_list = [(item[0], sublist[1], sublist[0]) for item in sorted_allLayers for sublist in item[1]]

        # Sort by the length of the sublists
        sorted_flattened_list = sorted(flattened_list, key=lambda x: len(x[1]))
        
        return sorted_flattened_list
    
    def getCubesNeededSetsDependend(self):
        """
        Divide cubes into quarters based on their positions in the layer and return all subsets sorted by size, smallest first.
        Filters out quarters that have dependent cubes.
        """
        allLayerQuarters = {}
        for layer in range(3):
            # Identify the axes for the layer
            axes = self.layer2xyz[layer]
            axis_1, axis_2 = axes[0], axes[1]

            # Divide cubes into four quarters based on their positions in the layer
            quarters = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
            layerCoord = self.position[self.cubeID][layer]
            for i in self.getLayerCubes(layer):
                coord = self.position[i]
                if coord[layer] == layerCoord:  # Ensure the cube is in the current layer
                    x, y = coord[axis_1], coord[axis_2]
                    cube_x = self.position[self.cubeID][axis_1]
                    cube_y = self.position[self.cubeID][axis_2]
                    # Assign cubes to quarters
                    if x >= cube_x and y >= cube_y:
                        quarters["Q1"].append(i)  # Top-right quarter
                    if x <= cube_x and y >= cube_y:
                        quarters["Q2"].append(i)  # Bottom-right quarter
                    if x >= cube_x and y <= cube_y:
                        quarters["Q3"].append(i)  # Top-left quarter
                    if x <= cube_x and y <= cube_y:
                        quarters["Q4"].append(i)  # Bottom-left quarter

            # Filter out quarters with dependent cubes and create sorted list
            filtered_quarters = []
            for quarter_name, cube_list in quarters.items():
                if len(cube_list) > 1 and not self.haveDependentCubes(cube_list):
                    filtered_quarters.append((quarter_name, cube_list))
            
            # Sort the filtered quarters by length
            sorted_quarters = sorted(filtered_quarters, key=lambda q: len(q[1]))
            allLayerQuarters[layer] = [(q, sorted(cubes)) for q, cubes in sorted_quarters]

        sorted_allLayers = sorted(allLayerQuarters.items(), key=lambda q: len(q[1]))

        # Flatten the list (no need to filter sublists with one element as it's done above)
        flattened_list = [(item[0], sublist[1], sublist[0]) for item in sorted_allLayers for sublist in item[1]]

        # Sort by the length of the sublists
        sorted_flattened_list = sorted(flattened_list, key=lambda x: len(x[1]))
        
        return sorted_flattened_list

    def getCubesNeededSetsDependend_Bounds(self):
        """
        Divide cubes into quarters based on their positions in the layer and return all subsets 
        sorted by size, smallest first. Each subset includes its bounds.
        """
        allLayerQuarters = {}
        for layer in range(3):
            axes = self.layer2xyz[layer]
            axis_1, axis_2 = axes[0], axes[1]

            # Dictionary to store quarters and their bounds
            quarters = {"Q1": {"cubes": [], "bounds": None},
                        "Q2": {"cubes": [], "bounds": None},
                        "Q3": {"cubes": [], "bounds": None},
                        "Q4": {"cubes": [], "bounds": None}}
            
            layerCoord = self.position[self.cubeID][layer]
            cube_x = self.position[self.cubeID][axis_1]
            cube_y = self.position[self.cubeID][axis_2]

            for i in self.getLayerCubes(layer):
                coord = self.position[i]
                if coord[layer] == layerCoord:
                    x, y = coord[axis_1], coord[axis_2]
                    
                    # Assign cubes to quarters with their bounds
                    if x >= cube_x and y >= cube_y:
                        quarters["Q1"]["cubes"].append(i)
                        quarters["Q1"]["bounds"] = [(axis_1, -1), (axis_2, -1)]
                    if x <= cube_x and y >= cube_y:
                        quarters["Q2"]["cubes"].append(i)
                        quarters["Q2"]["bounds"] = [(axis_1, +1), (axis_2, -1)]
                    if x >= cube_x and y <= cube_y:
                        quarters["Q3"]["cubes"].append(i)
                        quarters["Q3"]["bounds"] = [(axis_1, -1), (axis_2, +1)]
                    if x <= cube_x and y <= cube_y:
                        quarters["Q4"]["cubes"].append(i)
                        quarters["Q4"]["bounds"] = [(axis_1, +1), (axis_2, +1)]

            # Filter out quarters with dependent cubes
            filtered_quarters = []
            for quarter_name, quarter_data in quarters.items():
                cube_list = quarter_data["cubes"]
                bounds = quarter_data["bounds"]
                if len(cube_list) > 1 and not self.haveDependentCubes(cube_list):
                    filtered_quarters.append((quarter_name, cube_list, bounds))
            
            # Sort the filtered quarters by length of cube list
            sorted_quarters = sorted(filtered_quarters, key=lambda q: len(q[1]))
            allLayerQuarters[layer] = sorted_quarters

        sorted_allLayers = sorted(allLayerQuarters.items(), key=lambda q: len(q[1]))

        # Flatten the list and include bounds
        flattened_list = [(item[0], sublist[1], sublist[0], sublist[2]) 
                        for item in sorted_allLayers 
                        for sublist in item[1]]

        # Sort by the length of the cube lists
        sorted_flattened_list = sorted(flattened_list, key=lambda x: len(x[1]))
        
        return sorted_flattened_list


    def getCubesNeeded_Bounds(self):
        """
        Divide cubes into quarters based on their positions in the layer and return all subsets 
        sorted by size, smallest first. Each subset includes its bounds.
        """
        allLayerQuarters = {}
        for layer in range(3):
            axes = self.layer2xyz[layer]
            axis_1, axis_2 = axes[0], axes[1]

            # Dictionary to store quarters and their bounds
            quarters = {"Q1": {"cubes": [], "bounds": None},
                        "Q2": {"cubes": [], "bounds": None},
                        "Q3": {"cubes": [], "bounds": None},
                        "Q4": {"cubes": [], "bounds": None}}
            
            layerCoord = self.position[self.cubeID][layer]
            cube_x = self.position[self.cubeID][axis_1]
            cube_y = self.position[self.cubeID][axis_2]

            for i in self.getLayerCubes(layer):
                coord = self.position[i]
                if coord[layer] == layerCoord:
                    x, y = coord[axis_1], coord[axis_2]
                    
                    # Assign cubes to quarters with their bounds
                    if x >= cube_x and y >= cube_y:
                        quarters["Q1"]["cubes"].append(i)
                        quarters["Q1"]["bounds"] = [(axis_1, -1), (axis_2, -1)]
                    if x <= cube_x and y >= cube_y:
                        quarters["Q2"]["cubes"].append(i)
                        quarters["Q2"]["bounds"] = [(axis_1, +1), (axis_2, -1)]
                    if x >= cube_x and y <= cube_y:
                        quarters["Q3"]["cubes"].append(i)
                        quarters["Q3"]["bounds"] = [(axis_1, -1), (axis_2, +1)]
                    if x <= cube_x and y <= cube_y:
                        quarters["Q4"]["cubes"].append(i)
                        quarters["Q4"]["bounds"] = [(axis_1, +1), (axis_2, +1)]

            # Filter out quarters with less than 2 cubes
            filtered_quarters = []
            for quarter_name, quarter_data in quarters.items():
                cube_list = quarter_data["cubes"]
                bounds = quarter_data["bounds"]
                if len(cube_list) > 1:
                    filtered_quarters.append((quarter_name, cube_list, bounds))
            
            # Sort the filtered quarters by length of cube list
            sorted_quarters = sorted(filtered_quarters, key=lambda q: len(q[1]))
            allLayerQuarters[layer] = sorted_quarters

        sorted_allLayers = sorted(allLayerQuarters.items(), key=lambda q: len(q[1]))

        # Flatten the list and include bounds
        flattened_list = [(item[0], sublist[1], sublist[0], sublist[2]) 
                        for item in sorted_allLayers 
                        for sublist in item[1]]

        # Sort by the length of the cube lists
        sorted_flattened_list = sorted(flattened_list, key=lambda x: len(x[1]))
        
        return sorted_flattened_list
    


    def getCubesNeeded_Bounds_CSA(self):
        """
        Divide cubes into quarters based on their positions in the layer and return all subsets 
        sorted by size, smallest first. Each subset includes its bounds.
        """
        allLayerQuarters = {}
        for layer in range(3):
            axes = self.layer2xyz[layer]
            axis_1, axis_2 = axes[0], axes[1]

            # Dictionary to store quarters and their bounds
            quarters = {"Q1": {"cubes": [], "bounds": [2,2,2]},
                        "Q2": {"cubes": [], "bounds": [2,2,2]},
                        "Q3": {"cubes": [], "bounds": [2,2,2]},
                        "Q4": {"cubes": [], "bounds": [2,2,2]}}
            
            layerCoord = self.position[self.cubeID][layer]
            cube_x = self.position[self.cubeID][axis_1]
            cube_y = self.position[self.cubeID][axis_2]

            for i in self.getLayerCubes(layer):
                coord = self.position[i]
                if coord[layer] == layerCoord:
                    x, y = coord[axis_1], coord[axis_2]
                    
                    # Assign cubes to quarters with their bounds
                    if x >= cube_x and y >= cube_y:
                        quarters["Q1"]["cubes"].append(i)
                        quarters["Q1"]["bounds"][axis_1] = -1
                        quarters["Q1"]["bounds"][axis_2] = -1
                    if x <= cube_x and y >= cube_y:
                        quarters["Q2"]["cubes"].append(i)
                        quarters["Q2"]["bounds"][axis_1] = +1
                        quarters["Q2"]["bounds"][axis_2] = -1
                    if x >= cube_x and y <= cube_y:
                        quarters["Q3"]["cubes"].append(i)
                        quarters["Q3"]["bounds"][axis_1] = -1
                        quarters["Q3"]["bounds"][axis_2] = +1 
                    if x <= cube_x and y <= cube_y:
                        quarters["Q4"]["cubes"].append(i)
                        quarters["Q4"]["bounds"][axis_1] = +1
                        quarters["Q4"]["bounds"][axis_2] = +1                        
                        

            # Filter out quarters with less than 2 cubes
            filtered_quarters = []
            for quarter_name, quarter_data in quarters.items():
                cube_list = quarter_data["cubes"]
                bounds = quarter_data["bounds"]
                if len(cube_list) > 1:
                    filtered_quarters.append((quarter_name, cube_list, bounds))
            
            # Sort the filtered quarters by length of cube list
            sorted_quarters = sorted(filtered_quarters, key=lambda q: len(q[1]))
            allLayerQuarters[layer] = sorted_quarters

        sorted_allLayers = sorted(allLayerQuarters.items(), key=lambda q: len(q[1]))

        # Flatten the list and include bounds
        flattened_list = [(item[0], sublist[1], sublist[0], sublist[2]) 
                        for item in sorted_allLayers 
                        for sublist in item[1]]

        # Sort by the length of the cube lists
        sorted_flattened_list = sorted(flattened_list, key=lambda x: len(x[1]))
        
        return sorted_flattened_list






    def haveDependentCubes(self, checkCubes):
        for cube in checkCubes: 
            if len(self.getDependentCubes(cube)) > 0 and cube != self.cubeID:
                return True
        return False

    def getDependentCubes(self, checkCube):
        graph = ProgrammableCubes(np.copy(self.position)).cube_neighbours

        visited = []
        newCubes = queue.Queue()
        newCubes.put(self.cubeID)

        while not newCubes.empty():
            cube = newCubes.get()
            if cube not in visited and cube != checkCube:
                visited.append(cube)
                for neighbour in graph[cube]:
                    if neighbour not in visited and neighbour != checkCube:
                        newCubes.put(neighbour)
        
        # Get all cubes that weren't visited (excluding checkCube)
        notVisited = [cube for cube in range(len(self.position)) 
                    if cube not in visited and cube != checkCube]
        
        return notVisited
    
    def isLink(self): 
        graph = ProgrammableCubes(np.copy(self.position)).cube_neighbours

        links = graph[self.cubeID]
        graph[self.cubeID] = []
        for link in links: 
            if self.cubeID in graph[link]: 
                graph[link].remove(self.cubeID)
        
        visited = []

        visited = []
        newCubes = queue.Queue()
        newCubes.put(links[0])

        while newCubes.qsize() > 0:
            cube = newCubes.get()
            if(cube not in visited):
                visited.append(cube)
                for neighbour in graph[cube]:
                    if neighbour not in visited:
                        newCubes.put(neighbour)

        return len(visited) == len(self.position) - 1