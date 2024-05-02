import esper
from src.ecs.components.c_surface import CSurface


def system_flashing_text(world: esper.World, entity: int, interval: float, accumulated_time: float):
    c_surface = world.component_for_entity(entity, CSurface)

    if c_surface:
        c_surface.is_visible = (int(accumulated_time / interval) % 2) == 0
