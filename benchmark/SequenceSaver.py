import os
import json
import numpy as np

class SequenceSaver:
    def __init__(self, movesSequence=[], problem="no_prob_name", solverUsed="noSolver"):
        self.moveSequence = movesSequence  # list of tuples (cubeId, moveId)
        self.problem = problem  # string
        self.solverUsed = solverUsed  # string
        self.saveFolder = "moveSequences/"

    def saveSequenceToJson(self):
        # Create the directory if it doesn't exist
        if not os.path.exists(self.saveFolder):
            os.makedirs(self.saveFolder)

        # Create the base filename
        base_filename = f"{self.problem}_{self.solverUsed}.json"
        filename = os.path.join(self.saveFolder, base_filename)

        # Check if the file already exists and append a number if it does
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(self.saveFolder, f"{self.problem}_{self.solverUsed}_{counter}.json")
            counter += 1

        # Convert int64 to int in moveSequence
        moveSequence = [(int(cubeId), int(moveId)) for cubeId, moveId in self.moveSequence]

        # Create the data dictionary
        data = {
            "solverUsed": self.solverUsed,
            "problem": self.problem,
            "moveSequence": moveSequence
        }

        # Write the data to a JSON file
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Sequence saved to {filename}")
        return filename

    def loadSequenceFromJson(self, filename):
        # Read the data from a JSON file
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        # Extract the moveSequence
        loadedSequence = data.get("moveSequence", [])

        moveSequence = []

        for m in loadedSequence:
            moveSequence.append((np.int64(m[0]), np.int64(m[1])))

        return moveSequence