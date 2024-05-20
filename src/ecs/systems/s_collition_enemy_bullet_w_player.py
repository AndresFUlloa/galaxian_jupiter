from typing import Callable
import pygame

import esper
from src.create.prefab_creator_play import create_explosion, create_player_explosion
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_emeny_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_score import CTagScore
from src.engine.service_locator import ServiceLocator


def system_collision_bullet_player(world: esper.World, exp_info: dict,_subtract_lives: Callable[[esper.World], None]):
    player_components = world.get_components(CSurface, CTransform, CTagPlayer)
    enemy_bullet = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for bullet_entity, (b_s, b_t, _,) in enemy_bullet:
        pl_rect = CSurface.get_area_relative(b_s.area, b_t.pos)
        for player_entity, (c_s, c_t, c_enemy) in player_components:
            ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
            if ene_rect.colliderect(pl_rect):
                #world.delete_entity(player_entity)
                world.delete_entity(bullet_entity)
                create_player_explosion(world, c_t.pos, exp_info)
                _subtract_lives(world)
                print("lives remaining:"+str(world.get_component(CTagPlayer)[0][1].lives))
                if world.get_component(CTagPlayer)[0][1].lives ==0 :
                    player_bullet=world.get_component(CTagPlayerBullet)[0][0]
                    #world.delete_entity(player_entity)
                    world.component_for_entity(player_entity, CSurface).is_visible = False
                    world.component_for_entity(player_bullet, CSurface).is_visible = False
                    #world.get_component(CPlayState)[0][1].state= PlayState.GAME_OVER
                    
                    
                
                