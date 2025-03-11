
from framework.programmable_cubes_UDP import programmable_cubes_UDP
from solver.CSASolver import Solver as CSASolver
from benchmark.SolutionCreator import fitness
from solver.IPASolverREFACTOR import Solver as IPASolver
from utils.EvaluationUtils import correctCubes2
from utils.ConfigurationUtils import movesToPositions
import numpy as np

iss = programmable_cubes_UDP('ISS')
cube_pos1 = iss.initial_cube_pos
cube_pos2 = iss.target_cube_positions
init_types = iss.initial_cube_types
targetTypes = iss.target_cube_types



csa_move_sequence = CSASolver(cube_pos1,cube_pos2,init_types,targetTypes).solve()
ipa_move_sequence = IPASolver(cube_pos1,cube_pos2,init_types,targetTypes).solve()

csa_correct = correctCubes2(np.copy(movesToPositions(csa_move_sequence,cube_pos1)),np.copy(cube_pos2),np.copy(init_types),np.copy(targetTypes))
ipa_correct = correctCubes2(movesToPositions(ipa_move_sequence,cube_pos1),cube_pos2,init_types,targetTypes)

csa_fitness = fitness(csa_move_sequence,0)
ipa_fitness = fitness(ipa_move_sequence,0)

print("CSA Correct Cube Positions: " + str(csa_correct))
print("IPA Correct Cube Positions: " + str(ipa_correct))
print("CSA Fitness: " + str(csa_fitness))
print("IPA Fitness: " + str(ipa_fitness))

