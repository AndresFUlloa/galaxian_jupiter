import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface


def system_blinking(world: esper.World, accumulated_time: float):
    components = world.get_components(CSurface, CBlink)

    c_s: CSurface
    c_b: CBlink

    for _, (c_s, c_b) in components:
        c_s.is_visible = (int(accumulated_time / c_b.interval) % 2) == 0
