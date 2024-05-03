import pygame

from src.create.prefab_creator import create_player, create_input_player
from src.create.prefab_creator_interface import create_text, TextAlignment
from src.create.prefab_creator_play import create_enemies
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_enemies_bounce import system_enemies_bounce
from src.ecs.systems.s_flashing_text import system_flashing_text
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_boundaries import system_player_boundaries
from src.engine.scenes.scene import Scene
from src.utilities.config_loader import load_config_file


class PlayScene(Scene):
    def __init__(self, level_path: str, engine: 'src.engine.game_engine') -> None:
        super().__init__(engine)
        self.paused_text_entity = None
        self.paused_text_surface = None
        self.player_cfg = load_config_file('assets/cfg/player.json')
        self.lvl_cfg = level_path
        self.screen = engine.screen
        self.window_cfg = engine.window_cfg
        self.current_lvl = 0
        self.lvl_cfg = load_config_file('assets/cfg/lvls.json')[self.current_lvl]
        self.enemies_cfg = load_config_file('assets/cfg/enemies.json')
        self._paused = False

        self._accumulated_time = 0.0

    def do_create(self):
        super().do_create()
        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._paused = False

        paused_position = pygame.Vector2(
            self.screen.get_width() // 2,
            (self.screen.get_height() // 2 + 30)
        )
        self.paused_text_entity = create_text(
            self.ecs_world, "PAUSED",
            12,
            pygame.Color(255, 50, 50),
            paused_position,
            TextAlignment.CENTER
        )
        self.paused_text_surface = self.ecs_world.component_for_entity(self.paused_text_entity, CSurface)
        self.paused_text_surface.is_visible = self._paused

        create_input_player(self.ecs_world)
        create_enemies(self.ecs_world, self.enemies_cfg, pygame.Vector2(self.lvl_cfg['enemies_velocity'], 0))

    def do_update(self, delta_time: float):
        super().do_update(delta_time)
        self._accumulated_time += delta_time

        if self._paused:
            system_flashing_text(self.ecs_world, self.paused_text_entity, 0.5, self._accumulated_time)
        else:
            system_animation(self.ecs_world, delta_time)
            system_enemies_bounce(self.ecs_world, self.screen, self.window_cfg['enemies_margin'])
            system_movement(self.ecs_world, delta_time)
            system_player_boundaries(self.ecs_world, self._player_entity, self.screen, self.window_cfg['player_margin'])

    def do_clean(self):
        self._paused = False

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player_cfg['input_velocity']

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player_cfg['input_velocity']

        if c_input.name == "PAUSE":
            if c_input.phase == CommandPhase.START:
                self._paused = not self._paused
                self.paused_text_surface.is_visible = self._paused