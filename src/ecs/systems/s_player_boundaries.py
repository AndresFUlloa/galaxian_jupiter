import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_player_boundaries(world: esper.World, player_entity: int, screen: pygame.Surface, margin: int):
    c_t: CTransform
    c_s: CSurface
    c_t = world.component_for_entity(player_entity, CTransform)
    c_s = world.component_for_entity(player_entity, CSurface)

    if c_t.pos.x < margin:
        c_t.pos.x = margin

    if c_t.pos.x + c_s.surf.get_width() > screen.get_width() - margin:
        c_t.pos.x = screen.get_width() - margin - c_s.surf.get_width()
