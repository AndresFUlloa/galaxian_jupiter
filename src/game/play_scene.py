import pygame

from src.create.prefab_creator import create_player, create_input_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_boundaries import system_player_boundaries
from src.engine.scenes.scene import Scene
from src.utilities.config_loader import load_config_file


class PlayScene(Scene):
    def __init__(self, level_path: str, engine: 'src.engine.game_engine') -> None:
        super().__init__(engine)
        self.player_cfg = load_config_file('assets/cfg/player.json')
        self.lvl_cfg = level_path
        self.screen = engine.screen
        self.window_cfg = engine.window_cfg
        self._paused = False

    def do_create(self):
        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._paused = False
        create_input_player(self.ecs_world)

    def do_update(self, delta_time: float):
        system_movement(self.ecs_world, delta_time)
        system_player_boundaries(self.ecs_world, self._player_entity, self.screen, self.window_cfg['margin'])

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
