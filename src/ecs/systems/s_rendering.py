import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar


def system_rendering(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    c_t: CTransform
    c_s: CSurface

    for entity, (c_t, c_s) in components:
        if not c_s.is_visible:
            continue

        screen.blit(c_s.surf, c_t.pos, area=c_s.area)

