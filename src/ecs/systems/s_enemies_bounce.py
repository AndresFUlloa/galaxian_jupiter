import pygame

import esper
from src.ecs.components.c_enemies_stop_motion import CEnemiesStopMotion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemies_bounce(world: esper.World, screen: pygame.Surface, margin: int, stop_motion_entity: int):
    components = world.get_components(CTransform, CSurface, CVelocity, CTagEnemy)

    c_t: CTransform
    c_s: CSurface
    c_v: CVelocity

    for enemy_entity, (c_t, c_s, c_v, _) in components:
        rect = c_s.area.copy()
        rect.topleft = c_t.pos
        if rect.right > screen.get_width() - margin or c_t.pos.x < margin:
            c_v.vel.x *= -1
            world.component_for_entity(stop_motion_entity, CEnemiesStopMotion).prev_velocity = c_v.vel.x
            return
