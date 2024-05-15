import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.systems.s_player_bullet_movement import _search_charged_bullet


def system_player_boundaries(world: esper.World, player_entity: int, screen: pygame.Surface, margin: int):
    c_t = world.component_for_entity(player_entity, CTransform)
    c_s = world.component_for_entity(player_entity, CSurface)

    charged_bullet_entity = _search_charged_bullet(world)
    if charged_bullet_entity is not None:
        c_b_t = world.component_for_entity(charged_bullet_entity, CTransform)
        c_b_s = world.component_for_entity(charged_bullet_entity, CSurface)
    else:
        c_b_t = c_b_s = None

    if c_t.pos.x < margin:
        c_t.pos.x = margin
        if c_b_t is not None:
            _adjust_bullet_position(c_t, c_s, c_b_t, c_b_s)

    if c_t.pos.x + c_s.surf.get_width() > screen.get_width() - margin:
        c_t.pos.x = screen.get_width() - margin - c_s.surf.get_width()
        if c_b_t is not None:
            _adjust_bullet_position(c_t, c_s, c_b_t, c_b_s)


def _adjust_bullet_position(c_t: CTransform, c_s: CSurface, c_b_t: CTransform, c_b_s: CSurface):
    play_rect = c_s.surf.get_rect().copy()
    play_rect.topleft = c_t.pos.copy()
    c_b_t.pos.x = play_rect.midtop[0] - c_b_s.surf.get_width() / 2 + 1
