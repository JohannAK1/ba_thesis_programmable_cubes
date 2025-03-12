from framework.programmable_cubes_UDP import programmable_cubes_UDP
from animation.PosSaver import SinglePositionSaver


iss = programmable_cubes_UDP('ISS')

cube_pos1 = iss.initial_cube_pos
cube_pos2 = iss.target_cube_positions


SinglePositionSaver(cube_pos1, iss.initial_cube_types, 'Initial Position').save_fixed_view_figure('images/initial_position.png')
SinglePositionSaver(cube_pos2, iss.target_cube_types, 'Target Position').save_fixed_view_figure('images/target_position.png')

