import random

import pygame

import esper
from src.create.prefab_creator import create_sprite
from src.create.prefab_creator_interface import create_text, TextAlignment
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_enemies_stop_motion import CEnemiesStopMotion
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_emeny_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_level_flag import CTagLevelFlag
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.components.tags.c_tag_score import CTagScore
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_square
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def create_enemies(world: esper.World, enemies_info: list[dict]):

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
                enemy_sprite = create_sprite(world, pygame.Vector2(x_pos2, y_pos), pygame.Vector2(0,0), surf, animations=animations)
                world.add_component(enemy_sprite, CTagEnemy(enemy_info["points"]))
                world.add_component(enemy_sprite, CEnemyState())
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


def create_player_bullet(world: esper.World, bullet_info: dict, player_entity: int):
    c_t: CTransform = world.component_for_entity(player_entity, CTransform)
    c_s: CSurface = world.component_for_entity(player_entity, CSurface)
    c_v: CVelocity = world.component_for_entity(player_entity, CVelocity)

    player_rect = c_s.surf.get_rect()
    player_rect.topleft = c_t.pos
    pos = pygame.Vector2(player_rect.midtop)
    pos.x -= bullet_info["size"]["x"] / 2 - 1
    pos.y -= bullet_info["size"]["y"] - 1

    bullet_entity = create_square(world, pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"]),
                                  pos, c_v.vel.copy(),
                                  pygame.Color(bullet_info["color"]["r"], bullet_info["color"]["g"],
                                               bullet_info["color"]["b"]))
    world.add_component(bullet_entity, CTagPlayerBullet())
    world.add_component(bullet_entity, CBulletState())
    return bullet_entity


def create_enemy_bullet(world: esper.World, bullet_info: dict, enemy_entity: int):
    c_t: CTransform = world.component_for_entity(enemy_entity, CTransform)
    c_s: CSurface = world.component_for_entity(enemy_entity, CSurface)
    c_v: CVelocity = world.component_for_entity(enemy_entity, CVelocity)

    enemy_rect = c_s.surf.get_rect()
    enemy_rect.topleft = c_t.pos
    pos = pygame.Vector2(enemy_rect.midbottom)
    pos.x -= bullet_info["size"]["x"] / 2 - 1
    pos.y -= bullet_info["size"]["y"] - 1

    bullet_entity = create_square(world, pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"]),
                                  pos, c_v.vel.copy(),
                                  pygame.Color(bullet_info["color"]["r"], bullet_info["color"]["g"],
                                               bullet_info["color"]["b"]))
    world.add_component(bullet_entity, CTagEnemyBullet())
    world.add_component(bullet_entity, CBulletState())
    return bullet_entity


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    pos = pygame.Vector2(pos.x,
                         pos.y)
    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, pos, vel, explosion_surface, animations=explosion_info['animations'])
    world.add_component(explosion_entity, CTagExplosion())
    ServiceLocator.sounds_service.play(explosion_info["sound"])


def create_paused_text(world: esper.World, screen: pygame.Surface) -> int:
    paused_position = pygame.Vector2(
        screen.get_width() // 2,
        (screen.get_height() // 2 + 30)
    )
    entity = create_text(
        world,
        "PAUSED",
        12,
        pygame.Color(255, 50, 50),
        paused_position,
        TextAlignment.CENTER
    )
    world.add_component(entity, CBlink(0.5))

    return entity


def create_header(world: esper.World, level_info: dict, player_info: dict):
    header_pos_y = 10
    header_value_pos_y = 20

    create_text(
        world,
        "1UP",
        8,
        pygame.Color(255, 50, 50),
        pygame.Vector2(50, header_pos_y),
        TextAlignment.LEFT
    )
    current_score_text = create_text(
        world,
        "00",
        8,
        pygame.Color(255, 255, 255),
        pygame.Vector2(65, header_value_pos_y),
        TextAlignment.LEFT
    )
    world.add_component(current_score_text, CTagScore())

    create_text(
        world, "HI-SCORE",
        8, pygame.Color(255, 50, 50),
        pygame.Vector2(100, header_pos_y),
        TextAlignment.LEFT
    )
    create_text(
        world,
        "5000",
        8,
        pygame.Color(0, 113, 239),
        pygame.Vector2(125, header_value_pos_y),
        TextAlignment.LEFT
    )

    flag_surface = ServiceLocator.images_service.get(level_info['flag']['image'])
    flag_position = pygame.Vector2(
        level_info['flag']['position']['x'],
        level_info['flag']['position']['y']
    )

    flag_entity = create_sprite(world, flag_position, pygame.Vector2(0, 0), flag_surface)
    world.add_component(flag_entity, CTagLevelFlag())

    life_surface = ServiceLocator.images_service.get(level_info['life']['image'])

    for i in range(player_info['lives']):
        pos_x = level_info['life']['position']['x'] + life_surface.get_width() * i

        life_position = pygame.Vector2(
            pos_x + i,
            level_info['life']['position']['y']
        )
        life_entity = create_sprite(world, life_position, pygame.Vector2(0, 0), life_surface)
        world.add_component(life_entity, CTagLife())

