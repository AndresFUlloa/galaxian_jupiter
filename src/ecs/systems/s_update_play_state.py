import esper, pygame
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.ecs.components.c_ready_wait_dp import CReadyWaitDP
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_game_over_char import CTagGameOverChar
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_charge_bullet import system_charge_bullet
from src.ecs.systems.s_collision_player_bullet_w_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collition_enemy_bullet_w_player import system_collision_bullet_player
from src.ecs.systems.s_enemies_movement import _change_enemies_velocity, system_enemies_movement
from src.ecs.systems.s_enemy_shooting import system_enemy_shooting
from src.ecs.systems.s_explosion_time import system_explosion_time
from src.ecs.systems.s_level_change import system_level_change
from src.ecs.systems.s_player_boundaries import system_player_boundaries
from src.ecs.systems.s_player_bullet_boundaries import system_player_bullet_boundaries
from src.ecs.systems.s_update_player_bullet_movement import system_update_player_bullet_movement
from src.ecs.systems.system_stop_game_over import system_stop_game_over
from src.engine.service_locator import ServiceLocator
from src.ecs.systems.s_movement import system_movement
from src.ecs.components.tags.c_tag_ready_text import CTagReadyText
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator_interface import create_text, TextAlignment
from src.create.prefab_creator_play import create_enemies, create_player_bullet, create_game_over
from src.ecs.components.c_surface import CSurface


def system_update_play_state(world: esper.World, delta_time: float, screen: pygame.Surface, level_info: dict,
                             accumulated_time):
    c_p_s = world.get_component(CPlayState)[0][1]
    c_p_s.current_time += delta_time
    game_times_cfg = ServiceLocator.jsons_service.get('assets/cfg/game_times.json')
    if world.get_component(CTagPlayer)[0][1].lives == 0:
        c_p_s.state = PlayState.GAME_OVER
    system_movement(world, delta_time, c_p_s.state in [PlayState.PAUSE, PlayState.GAME_OVER])

    if c_p_s.state == PlayState.START:
        if c_p_s.current_time < game_times_cfg["ready_time_init"]:
            return False
        if game_times_cfg["ready_time_init"] <= c_p_s.current_time < game_times_cfg["ready_time_enemy"]:
            if len(world.get_components(CTagReadyText)) == 0:
                ready_entity = create_text(world, "READY", 14, pygame.Color(234, 61, 1), pygame.Vector2(128, 200),
                                           TextAlignment.CENTER)
                ServiceLocator.sounds_service.play(level_info["ready"]["sound"])  # sonido de inicio del ready
                world.add_component(ready_entity, CTagReadyText())
            return False
        if game_times_cfg["ready_time_enemy"] <= c_p_s.current_time < game_times_cfg["ready_time_off"]:
            if len(world.get_components(CTagEnemy)) == 0:
                create_enemies(world, ServiceLocator.jsons_service.get("assets/cfg/enemies.json"))
            return False
        if game_times_cfg["ready_time_off"] <= c_p_s.current_time < game_times_cfg["ready_time_player"]:
            ready_entity = world.get_component(CTagReadyText)[0][0]
            world.component_for_entity(ready_entity, CSurface).is_visible = False
            return False

        player_entity = world.get_component(CTagPlayer)[0][0]
        world.component_for_entity(player_entity, CSurface).is_visible = True
        # _subtract_lives(world)
        create_player_bullet(
            world, ServiceLocator.jsons_service.get("assets/cfg/bullets.json")['player_bullet'], player_entity)
        _change_enemies_velocity(world, ServiceLocator.jsons_service.get(
            'assets/cfg/lvls.json')[c_p_s.current_lvl]['enemies_velocity'])
        c_p_s.state = PlayState.PLAY

        pygame.mixer.init()
        pygame.mixer.music.load('assets/snd/play_starfield-effect-1.ogg')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)

    if c_p_s.state == PlayState.PLAY:
        levels = ServiceLocator.jsons_service.get('assets/cfg/lvls.json')
        current_lvl = len(levels) - 1 if c_p_s.current_lvl >= len(levels) else c_p_s.current_lvl

        lvl_cfg = ServiceLocator.jsons_service.get('assets/cfg/lvls.json')[current_lvl]
        window_cfg = ServiceLocator.jsons_service.get('assets/cfg/window.json')
        explosion_cfg = ServiceLocator.jsons_service.get('assets/cfg/explosion.json')
        player_explosion_cfg = ServiceLocator.jsons_service.get('assets/cfg/player_explosion.json')
        bullets_cfg = ServiceLocator.jsons_service.get('assets/cfg/bullets.json')
        player_cfg = ServiceLocator.jsons_service.get('assets/cfg/player.json')
        player_entity = world.get_component(CTagPlayer)[0][0]

        system_animation(world, delta_time)
        system_enemies_movement(world, screen, delta_time, lvl_cfg['time_to_stop'], lvl_cfg['stopped_time'],
                                window_cfg['enemies_margin'])
        system_player_boundaries(world, player_entity, screen, window_cfg['player_margin'])
        system_player_bullet_boundaries(world, screen)
        system_collision_bullet_enemy(world, explosion_cfg)
        system_collision_bullet_player(world, player_explosion_cfg, _subtract_lives)
        system_explosion_time(world)
        system_charge_bullet(world, bullets_cfg["player_bullet"], player_entity)
        system_enemy_shooting(world, c_p_s.current_time, bullets_cfg['player_bullet'], lvl_cfg['shoot_time'])
        system_level_change(world, level_info, accumulated_time)
        system_update_player_bullet_movement(world, player_entity, player_cfg['input_velocity'])
        return False

    if c_p_s.state == PlayState.PLAYER_DEAD:
        lvl_cfg = ServiceLocator.jsons_service.get('assets/cfg/lvls.json')[c_p_s.current_lvl]
        window_cfg = ServiceLocator.jsons_service.get('assets/cfg/window.json')
        system_animation(world, delta_time)
        system_enemies_movement(world, screen, delta_time, lvl_cfg['time_to_stop'], lvl_cfg['stopped_time'],
                                window_cfg['enemies_margin'])
        system_explosion_time(world)
        if len(world.get_components(CTagExplosion)) == 0:
            c_r_w = world.get_component(CReadyWaitDP)[0][1]
            ready_entity = world.get_component(CTagReadyText)[0][0]
            c_r_s = world.component_for_entity(ready_entity, CSurface)
            if c_r_w.waited_time == 0:
                c_r_s.is_visible = True
            c_r_w.waited_time += delta_time
            if c_r_w.waited_time >= c_r_w.wait_time:
                c_r_w.waited_time = 0
                c_r_s.is_visible = False
                player_entity = world.get_component(CTagPlayer)[0][0]
                c_t_p = world.component_for_entity(player_entity, CTagPlayer)
                if c_t_p.lives > 0:
                    player_bullet_entity = world.get_component(CTagPlayerBullet)[0][0]
                    world.component_for_entity(player_entity, CSurface).is_visible = True
                    world.component_for_entity(player_bullet_entity, CSurface).is_visible = True
                    c_p_s.state = PlayState.PLAY
                else:
                    c_p_s.state = PlayState.GAME_OVER

    if c_p_s.state == PlayState.GAME_OVER:
        if len(world.get_components(CTagExplosion)) > 0:
            system_animation(world, delta_time)
            system_explosion_time(world)
            return False
        if len(world.get_components(CTagGameOverChar)) == 0:
            pygame.mixer.music.stop()
            ServiceLocator.sounds_service.play("assets/snd/game_over.ogg")
            create_game_over(world)
        stopped = system_stop_game_over(world)

        return stopped

    return False


def _subtract_lives(world: esper.World):
    world.get_component(CTagPlayer)[0][1].lives -= 1

    lives = world.get_components(CTagLife)

    if len(lives) == 0:
        return

    world.delete_entity(lives[-1][0])
