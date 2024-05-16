import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def system_player_bullet_boundaries(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayerBullet)

    c_t:CTransform
    c_s:CSurface
    for bullet_entity, (c_t, c_s, _) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos) 

        outside = False
        if bullet_rect.left < 0 or bullet_rect.right > screen_rect.width:  # si la parte izq del cuadrado es menor q 0, o si la parte derecha del cuadrado es superior al ancho de la pantalla
            outside =  True

        if bullet_rect.top < 0 or bullet_rect.bottom > screen_rect.height:
            outside =  True

        if outside:
            world.delete_entity(bullet_entity)