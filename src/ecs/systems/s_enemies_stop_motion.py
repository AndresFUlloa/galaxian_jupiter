import random

import esper
from src.ecs.components.c_enemies_stop_motion import CEnemiesStopMotion
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemies_stop_motion(world: esper.World, stop_motion_entity: int, time_to_sopt:dict,
                               stopped_time: dict, delta_time: float):
    c_e_s_m = world.component_for_entity(stop_motion_entity, CEnemiesStopMotion)
    c_v: CVelocity = world.get_components(CVelocity, CTagEnemy)[0][1][0]
    if c_e_s_m.stopped:
        c_e_s_m.remaining_stopped_time -= delta_time
        if c_e_s_m.remaining_stopped_time <= 0:
            c_e_s_m.stopped = False
            c_e_s_m.stopped_time = random.uniform(stopped_time['min'], stopped_time['max'])
            c_e_s_m.remaining_stopped_time = c_e_s_m.time_to_stop
            c_v.vel.x = c_e_s_m.prev_velocity
    else:
        c_e_s_m.remaining_time_to_stop -= delta_time
        if c_e_s_m.remaining_time_to_stop <= 0:
            c_e_s_m.stopped = True
            c_v.vel.x = 0
            c_e_s_m.time_to_stop = random.uniform(time_to_sopt['min'], time_to_sopt['max'])
            c_e_s_m.remaining_time_to_stop = c_e_s_m.time_to_stop

