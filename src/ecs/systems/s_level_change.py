import time

import pygame

import esper
from src.create.prefab_creator_interface import create_text, TextAlignment
from src.create.prefab_creator_play import create_flag, create_enemies
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_level_counter import CTagLevelCounter
from src.ecs.components.tags.c_tag_level_flag import CTagLevelFlag
from src.engine.service_locator import ServiceLocator


def system_level_change(world: esper.World, level_info: dict, accumulated_time: float):
    enemy_components = world.get_components(CTagEnemy)
    flag_components = world.get_components(CTagLevelFlag)
    counter_text_entity = world.get_component(CTagLevelCounter)[0][0]
    level_counter = world.component_for_entity(counter_text_entity, CTagLevelCounter)
    counter_text_surface = world.component_for_entity(counter_text_entity, CSurface)

    if len(enemy_components) == 0:
        if level_counter.level_finished_at is None:
            level_counter.level_finished_at = accumulated_time

        if (accumulated_time - level_counter.level_finished_at) < level_counter.delay_to_change:
            return

        if level_counter.level >= 5:
            if len(flag_components) > 1:
                for entity, _ in flag_components:
                    world.delete_entity(entity)
                    create_flag(world, level_info)
            counter_text_surface.is_visible = True
        elif level_counter.level < 5:
            last_flag_entity = flag_components[0][0]
            last_flag_surface = world.component_for_entity(last_flag_entity, CSurface)
            last_flag_transform = world.component_for_entity(last_flag_entity, CTransform)

            new_flag_position = pygame.Vector2(
                last_flag_transform.pos.x + (last_flag_surface.surf.get_width() * len(flag_components)),
                last_flag_transform.pos.y
            )

            create_flag(world, level_info, new_flag_position)

        level_counter.level += 1

        if counter_text_surface.is_visible:
            font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
            world.add_component(
                counter_text_entity,
                CSurface.from_text(str(level_counter.level).zfill(2), font, pygame.Color(255, 255, 255))
            )

        level_counter.level_finished_at = None
        create_enemies(world, ServiceLocator.jsons_service.get("assets/cfg/enemies.json"))

        print(f"Level {level_counter.level} started")

