import esper, pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_star import CTagStar

def system_update_stars(world:esper.World, delta_time:float, screen:pygame.Surface):
    components = world.get_components(CTransform, CTagStar, CSurface)
    c_t:CTransform
    c_t_s:CTagStar
    c_s:CSurface
    for _, (c_t, c_t_s, c_s) in components:
        if c_t.pos.y > screen.get_height():
            c_t.pos.y = 0
        _update_blink(c_t_s, c_s, delta_time)

def _update_blink(c_t_s:CTagStar, c_s:CSurface, delta_time:float):
    c_t_s.time_passed -= delta_time
    if c_t_s.time_passed <= 0:
        c_t_s.time_passed = c_t_s.blink_time
        c_s.is_visible = not c_s.is_visible



