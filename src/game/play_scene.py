import pygame

from src.create.prefab_creator import create_player, create_input_player
from src.create.prefab_creator_interface import create_text, TextAlignment
from src.create.prefab_creator_play import create_enemies, create_player_bullet, create_enemies_stop_motion, \
    create_paused_text, create_header
from src.create.prefab_debug import create_debug_input
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_ready_wait_dp import CReadyWaitDP
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_player_bullet_w_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_enemies_movement import system_enemies_movement

from src.ecs.systems.s_explosion_time import system_explosion_time
from src.ecs.systems.s_level_change import system_level_change
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
        self._editor_mode = False
        self.debug_text_surface = None
        self.game_over = False
      

    def load_files(self):
        super().load_files()
        self.player_cfg = ServiceLocator.jsons_service.get('assets/cfg/player.json')
        self.bullets_cfg = ServiceLocator.jsons_service.get('assets/cfg/bullets.json')
        self.explosion_cfg = ServiceLocator.jsons_service.get('assets/cfg/explosion.json')
        self.enemies_cfg = ServiceLocator.jsons_service.get('assets/cfg/enemies.json')
        self.level_cfg = ServiceLocator.jsons_service.get('assets/cfg/level.json')
        self.game_times_cfg = ServiceLocator.jsons_service.get('assets/cfg/game_times.json')

    def do_create(self):
        super().do_create()
        debug_text_ent = create_text(
            self.ecs_world,
            "[DEBUG MODE]",
            8,
            pygame.Color(51, 255, 51),
            pygame.Vector2(0, 0),
            TextAlignment.LEFT
        )
        self.debug_text_surface = self.ecs_world.component_for_entity(debug_text_ent, CSurface)
        self.debug_text_surface.is_visible = self._editor_mode

        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        create_header(self.ecs_world, self.level_cfg, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._paused = False
        self._stop_motion_entity = create_enemies_stop_motion(
            self.ecs_world, self.lvl_cfg['time_to_stop'], self.lvl_cfg['stopped_time'],
            self.lvl_cfg['enemies_velocity'])

        create_input_player(self.ecs_world)
        create_debug_input(self.ecs_world)
        self._play_state_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(self._play_state_entity, CPlayState())
        self.ecs_world.create_entity(CReadyWaitDP(self.game_times_cfg['ready_time_dead_player']))

    def do_update(self, delta_time: float):
        super().do_update(delta_time)
        self.game_over = system_update_play_state(
            self.ecs_world,
            delta_time,
            self.screen,
            self.level_cfg,
            self._accumulated_time
        )

    def do_clean(self):
        self._paused = False

    def do_action(self, c_input: CInputCommand):
        system_player_bullet_movement(self.ecs_world, c_input, self._player_entity)

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

        if c_input.name == "TOGGLE_EDITOR":
            if c_input.phase == CommandPhase.START:
                self._editor_mode = not self._editor_mode
                self.debug_text_surface.is_visible = self._editor_mode

        if self._editor_mode:
            self._do_editor_action(c_input)

        if c_input.name == "PLAYER_START":
            if c_input.phase == CommandPhase.START and self.game_over:
                self.switch_scene("MENU")

    def _do_editor_action(self, action: CInputCommand):
        if action.name == "KILL_ALL":
            components = self.ecs_world.get_components(CTagEnemy)
            for entity, _ in components:
                self.ecs_world.delete_entity(entity)