import random

import pygame

import esper
from src.create.prefab_creator import create_sprite
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemies_stop_motion import CEnemiesStopMotion
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_square
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def create_enemies(world: esper.World, enemies_info: list[dict], vel: pygame.Vector2):
    for enemy_info in enemies_info:
        animations: dict = None
        surf = ServiceLocator.images_service.get(enemy_info['image'])
        if "animations" in enemy_info:
            animations = enemy_info["animations"]

        y_pos = enemy_info['start_position']['y']
        x_pos = enemy_info['start_position']['x']
        for i in range(enemy_info['quantity']['rows']):
            x_pos2 = x_pos
            for j in range(enemy_info['quantity']['columns']):
                enemy_sprite = create_sprite(world, pygame.Vector2(x_pos2, y_pos), vel, surf, animations=animations)
                world.add_component(enemy_sprite, CTagEnemy())
                x_pos2 += enemy_info["distance"]['x']
            y_pos += enemy_info["distance"]['y']


def create_enemies_stop_motion(world: esper.World, time_to_stop: dict, stopped_time: dict, velocity: int):
    stop_motion_entity = world.create_entity()
    world.add_component(stop_motion_entity, CEnemiesStopMotion(
        random.uniform(time_to_stop['min'], time_to_stop['max']),
        random.uniform(stopped_time['min'], stopped_time['max']),
        velocity
    ))
    return stop_motion_entity


def create_player_bullet(world: esper.World, bullet_info: dict, num_bullet: int, player_entity: int):
    if len(world.get_components(CTagPlayerBullet)) >= num_bullet:
        return

    c_t: CTransform = world.component_for_entity(player_entity, CTransform)
    c_s: CSurface = world.component_for_entity(player_entity, CSurface)

    player_rect = c_s.surf.get_rect()
    player_rect.topleft = c_t.pos
    pos = pygame.Vector2(player_rect.midtop)
    pos.x -= bullet_info["size"]["x"] / 2
    pos.y -= bullet_info["size"]["y"]

    bullet_entity = create_square(world, pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"]),
                                  pos, pygame.Vector2(0, -bullet_info["velocity"]),
                                  pygame.Color(bullet_info["color"]["r"], bullet_info["color"]["g"],
                                               bullet_info["color"]["b"]))
    world.add_component(bullet_entity, CTagPlayerBullet())

