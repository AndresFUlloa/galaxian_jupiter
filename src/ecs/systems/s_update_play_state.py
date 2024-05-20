import esper, pygame
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_charge_bullet import system_charge_bullet
from src.ecs.systems.s_collision_player_bullet_w_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collition_enemy_bullet_w_player import system_collision_bullet_player
from src.ecs.systems.s_enemies_movement import _change_enemies_velocity, system_enemies_movement
from src.ecs.systems.s_enemy_shooting import  system_enemy_shooting
from src.ecs.systems.s_explosion_time import system_explosion_time
from src.ecs.systems.s_level_change import system_level_change
from src.ecs.systems.s_player_boundaries import system_player_boundaries
from src.ecs.systems.s_player_bullet_boundaries import system_player_bullet_boundaries
from src.engine.service_locator import ServiceLocator
from src.ecs.systems.s_movement import system_movement
from src.ecs.components.tags.c_tag_ready_text import CTagReadyText
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator_interface import create_text, TextAlignment
from src.create.prefab_creator_play import create_enemies, create_player_bullet
from src.ecs.components.c_surface import CSurface


def system_update_play_state(world: esper.World, delta_time: float, screen: pygame.Surface, level_info: dict, lvl_cfg: dict, accumulated_time):
    
    
    
    c_p_s = world.get_component(CPlayState)[0][1]
    c_p_s.current_time += delta_time
    game_times_cfg = ServiceLocator.jsons_service.get('assets/cfg/game_times.json')
    if world.get_component(CTagPlayer)[0][1].lives==0:
        c_p_s.state = PlayState.GAME_OVER
    system_movement(world, delta_time, c_p_s.state == PlayState.PAUSE)
    

    if c_p_s.state == PlayState.START:
        if c_p_s.current_time < game_times_cfg["ready_time_init"]:
            return
        if game_times_cfg["ready_time_init"] <= c_p_s.current_time < game_times_cfg["ready_time_enemy"]:
            if len(world.get_components(CTagReadyText)) == 0:
                ready_entity = create_text(world, "READY", 14, pygame.Color(234, 61, 1), pygame.Vector2(128, 200),
                                           TextAlignment.CENTER)
                world.add_component(ready_entity, CTagReadyText())
            return
        if game_times_cfg["ready_time_enemy"] <= c_p_s.current_time < game_times_cfg["ready_time_off"]:
            if len(world.get_components(CTagEnemy)) == 0:
                create_enemies(world, ServiceLocator.jsons_service.get("assets/cfg/enemies.json"))
            return
        if game_times_cfg["ready_time_off"] <= c_p_s.current_time < game_times_cfg["ready_time_player"]:
            ready_entity = world.get_component(CTagReadyText)[0][0]
            world.component_for_entity(ready_entity, CSurface).is_visible = False
            return

        player_entity = world.get_component(CTagPlayer)[0][0]
        world.component_for_entity(player_entity, CSurface).is_visible = True
        #_subtract_lives(world)
        create_player_bullet(
            world,
            ServiceLocator.jsons_service.get("assets/cfg/bullets.json")['player_bullet'],
            player_entity
        )
        _change_enemies_velocity(world, lvl_cfg['enemies_velocity'])
        c_p_s.state = PlayState.PLAY
    if c_p_s.state == PlayState.PLAY:
        window_cfg = ServiceLocator.jsons_service.get('assets/cfg/window.json')
        explosion_cfg = ServiceLocator.jsons_service.get('assets/cfg/explosion.json')
        player_explosion_cfg = ServiceLocator.jsons_service.get('assets/cfg/player_explosion.json')
        bullets_cfg = ServiceLocator.jsons_service.get('assets/cfg/bullets.json')
        player_entity = world.get_component(CTagPlayer)[0][0]

        system_animation(world, delta_time)
        system_enemies_movement(world, screen, delta_time, lvl_cfg['time_to_stop'], lvl_cfg['stopped_time'],
                                window_cfg['enemies_margin'])
        system_player_boundaries(world, player_entity, screen, window_cfg['player_margin'])
        system_player_bullet_boundaries(world, screen)
        system_collision_bullet_enemy(world, explosion_cfg)
        system_collision_bullet_player(world, player_explosion_cfg,_subtract_lives)
        system_explosion_time(world)
        system_charge_bullet(world, bullets_cfg["player_bullet"], player_entity)
        system_enemy_shooting(world,c_p_s.current_time,bullets_cfg['player_bullet'])
        system_level_change(world, level_info, accumulated_time)
    if c_p_s.state == PlayState.GAME_OVER:
        ready_entity = create_text(world, "GAME OVER", 14, pygame.Color(234, 61, 1), pygame.Vector2(128, 100),
                                           TextAlignment.CENTER)


def _subtract_lives(world: esper.World):
    world.get_component(CTagPlayer)[0][1].lives -= 1

    lives = world.get_components(CTagLife)

    if len(lives) == 0:
        return

    world.delete_entity(lives[-1][0])

