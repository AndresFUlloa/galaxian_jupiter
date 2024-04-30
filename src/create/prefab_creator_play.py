import pygame

import esper
from src.create.prefab_creator import create_sprite
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


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
