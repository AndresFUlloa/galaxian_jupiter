import pygame

import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_game_over_char import CTagGameOverChar


def system_stop_game_over(world: esper.World):
    components = world.get_components(CTransform, CVelocity, CTagGameOverChar)

    c_t: CTransform
    c_v: CVelocity
    c_t_g_o: CTagGameOverChar
    stopped = True
    for _, (c_t, c_v, c_t_g_o) in components:
        dis = c_t.pos.distance_squared_to(c_t_g_o.final_pos)
        if dis <= 1:
            c_t.pos = c_t_g_o.final_pos
            c_v.vel = pygame.Vector2(0, 0)
        else:
            stopped = False

    return stopped
