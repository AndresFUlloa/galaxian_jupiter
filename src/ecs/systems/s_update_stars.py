import esper, pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_star import CTagStar


def system_update_stars(world: esper.World, delta_time: float, screen: pygame.Surface):
    components = world.get_components(CTransform, CTagStar, CSurface)

    c_t: CTransform
    c_t_s: CTagStar
    c_s: CSurface

    for _, (c_t, c_t_s, c_s) in components:
        if c_t.pos.y > screen.get_height():
            c_t.pos.y = 0


