import pygame

from src.create.prefab_creator import create_player, create_input_player
from src.create.prefab_creator_play import create_enemies, create_player_bullet, create_enemies_stop_motion, \
    create_paused_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_player_bullet_w_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_enemies_movement import system_enemies_movement
from src.ecs.systems.s_explosion_time import system_explosion_time
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_boundaries import system_player_boundaries
from src.ecs.systems.s_player_bullet_boundaries import system_player_bullet_boundaries
from src.ecs.systems.s_shoot_bullet import system_shoot_bullet
from src.ecs.systems.s_charge_bullet import system_charge_bullet
from src.ecs.systems.s_player_bullet_movement import system_player_bullet_movement
from src.ecs.systems.s_update_play_state import system_update_play_state
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator



class PlayScene(Scene):
    def __init__(self, engine: 'src.engine.game_engine') -> None:
        super().__init__(engine)
        self.paused_text_entity = None
        self.paused_text_surface = None
        self.screen = engine.screen
        self.window_cfg = engine.window_cfg
        self.current_lvl = 0
        self.lvl_cfg = ServiceLocator.jsons_service.get('assets/cfg/lvls.json')[self.current_lvl]
        self._paused = False

    def load_files(self):
        super().load_files()
        self.player_cfg = ServiceLocator.jsons_service.get('assets/cfg/player.json')
        self.bullets_cfg = ServiceLocator.jsons_service.get('assets/cfg/bullets.json')
        self.explosion_cfg = ServiceLocator.jsons_service.get('assets/cfg/explosion.json')
        self.enemies_cfg = ServiceLocator.jsons_service.get('assets/cfg/enemies.json')

    def do_create(self):
        super().do_create()
        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._paused = False
        self._stop_motion_entity = create_enemies_stop_motion(
            self.ecs_world, self.lvl_cfg['time_to_stop'], self.lvl_cfg['stopped_time'],
            self.lvl_cfg['enemies_velocity'])

        create_input_player(self.ecs_world)
        #self._bullet_charged = create_player_bullet(self.ecs_world, self.bullets_cfg["player_bullet"],
        #                                            self._player_entity)
        #self._bullet_charged_v = self.ecs_world.component_for_entity(self._bullet_charged, CVelocity)
        #create_enemies(self.ecs_world, self.enemies_cfg, pygame.Vector2(self.lvl_cfg['enemies_velocity'], 0))
        self._play_state_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(self._play_state_entity,CPlayState())

    def do_update(self, delta_time: float):
        super().do_update(delta_time)
        system_update_play_state(self.ecs_world, delta_time, self.screen)

    def do_clean(self):
        self._paused = False

    def do_action(self, c_input: CInputCommand):
        system_player_bullet_movement(self.ecs_world, c_input, self.player_cfg["input_velocity"], self._player_entity)

        if c_input.name == "PLAYER_FIRE":
            c_p_s = self.ecs_world.component_for_entity(self._play_state_entity, CPlayState)
            if c_input.phase == CommandPhase.START and c_p_s.state == PlayState.PLAY:
                system_shoot_bullet(self.ecs_world, self.bullets_cfg['player_bullet']['velocity'])

        if c_input.name == "PAUSE":
            c_p_s = self.ecs_world.component_for_entity(self._play_state_entity, CPlayState)
            if c_input.phase == CommandPhase.START and (
                    c_p_s.state == PlayState.PLAY or c_p_s.state == PlayState.PAUSE):
                if c_p_s.state == PlayState.PLAY:
                    self.paused_text_entity = create_paused_text(self.ecs_world, self.screen)
                else:
                    self.ecs_world.delete_entity(self.paused_text_entity)

                c_p_s.state = PlayState.PAUSE if c_p_s.state == PlayState.PLAY else PlayState.PLAY
