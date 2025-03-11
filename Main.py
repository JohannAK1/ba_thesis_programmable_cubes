
from framework.programmable_cubes_UDP import programmable_cubes_UDP
from solver.CSASolver import Solver as CSASolver
from benchmark.SolutionCreator import fitness
from solver.IPASolver import Solver as IPASolver
from utils.EvaluationUtils import correctCubes2
from utils.ConfigurationUtils import movesToPositions
from animation.Animation import CubeAnimation

import numpy as np


# Loads the ISS Instance
iss = programmable_cubes_UDP('ISS')
cube_pos1 = iss.initial_cube_pos
cube_pos2 = iss.target_cube_positions
init_types = iss.initial_cube_types
targetTypes = iss.target_cube_types

# Solves the ISS Instance with the CSA and IPA Solver
csa_move_sequence = CSASolver(cube_pos1,cube_pos2,init_types,targetTypes).solve()
ipa_move_sequence = IPASolver(cube_pos1,cube_pos2,init_types,targetTypes).solve()

# Evaluates the solutions based on correct overlap 
csa_correct = correctCubes2(movesToPositions(csa_move_sequence,cube_pos1),cube_pos2,init_types,targetTypes)
ipa_correct = correctCubes2(movesToPositions(ipa_move_sequence,cube_pos1),cube_pos2,init_types,targetTypes)

# Evaluates the solutions based on fitness function
csa_fitness = fitness(csa_move_sequence,0)
ipa_fitness = fitness(ipa_move_sequence,0)

print("CSA Correct Cube Positions: " + str(csa_correct * 100) + "%")
print("IPA Correct Cube Positions: " + str(ipa_correct * 100) + "%")
print("CSA Fitness: " + str(csa_fitness))
print("IPA Fitness: " + str(ipa_fitness))

# Creates the animations of reconfiguration
CubeAnimation(csa_move_sequence,cube_pos1,init_types,10,20,'CSA').make_animation()
CubeAnimation(ipa_move_sequence,cube_pos1,init_types,10,20,'IPA').make_animation()

