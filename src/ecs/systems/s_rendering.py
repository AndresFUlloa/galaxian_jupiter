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
        if not world.has_component(entity, CTagStar):
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)
        else:
            c_t_s:CTagStar = world.component_for_entity(entity, CTagStar)
            if c_t_s.visible:
                screen.blit(c_s.surf, c_t.pos, area=c_s.area)

