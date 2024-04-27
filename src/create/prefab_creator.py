import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_player(world: esper.World, player_info: dict):
    player_surface = ServiceLocator.images_service.get(player_info['image'])
    player_size = player_surface.get_size()
    position = pygame.Vector2(
        player_info['start_pos']['x'] - player_size[0]/2, player_info['start_pos']['y'] - player_size[1])
    velocity = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, position, velocity, player_surface)
    world.add_component(player_entity, CTagPlayer())
