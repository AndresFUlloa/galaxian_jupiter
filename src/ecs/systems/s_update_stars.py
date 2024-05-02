import esper, pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar

def system_update_stars(world:esper.World, delta_time:float, screen:pygame.Surface):
    components = world.get_components(CTransform, CTagStar)
    c_t:CTransform
    c_t_s:CTagStar
    for _, (c_t, c_t_s) in components:
        if c_t.pos.y > screen.get_height():
            c_t.pos.y = 0
        _update_blink(c_t_s, delta_time)

def _update_blink(c_t_s:CTagStar, delta_time:float):
    c_t_s.time_passed -= delta_time
    if c_t_s.time_passed <= 0:
        c_t_s.time_passed = c_t_s.blink_time
        c_t_s.visible = not c_t_s.visible


