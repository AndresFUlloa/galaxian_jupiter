import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_bullet_state import CBulletState, BulletState


def system_player_boundaries(world: esper.World, player_entity: int, charged_bullet_entity: int, screen: pygame.Surface, margin: int):
    c_t: CTransform
    c_s: CSurface
    c_t = world.component_for_entity(player_entity, CTransform)
    c_s = world.component_for_entity(player_entity, CSurface)

    c_b_t: CTransform = None
    c_b_s: CSurface = None

    if charged_bullet_entity is not None and _get_num_charged_bullets(world) > 0:
        c_b_t = world.component_for_entity(charged_bullet_entity, CTransform)
        c_b_s = world.component_for_entity(charged_bullet_entity, CSurface)

    if c_t.pos.x < margin:
        c_t.pos.x = margin
        if c_b_t is not None:
            play_rect = c_s.surf.get_rect().copy()
            play_rect.topleft = c_t.pos.copy()
            c_b_t.pos.x = play_rect.midtop[0] - c_b_s.surf.get_width() / 2 + 1

    if c_t.pos.x + c_s.surf.get_width() > screen.get_width() - margin:
        c_t.pos.x = screen.get_width() - margin - c_s.surf.get_width()
        if c_b_s is not None:
            play_rect = c_s.surf.get_rect().copy()
            play_rect.topleft = c_t.pos.copy()
            c_b_t.pos.x = play_rect.midtop[0] - c_b_s.surf.get_width() / 2 + 1

def _get_num_charged_bullets(world:esper.World):
    components = world.get_components(CTagPlayerBullet, CBulletState)
    total = 0 
    for bullet_entity, (_, c_b_s) in components:
        if c_b_s.state == BulletState.IDLE:
            total += 1
    return total