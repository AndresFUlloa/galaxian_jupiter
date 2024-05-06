import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_collision_player_bullet_w_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_rendering import system_rendering
import src.engine.game_engine
from src.utilities.config_loader import load_config_file
from src.create.prefab_creator import create_stars
from src.ecs.systems.s_update_stars import system_update_stars


class Scene:
    def __init__(self, game_engine: 'src.engine.game_engine.GameEngine') -> None:
        self.ecs_world = esper.World()
        self._game_engine: src.engine.game_engine.GameEngine = game_engine
        self.screen_rect = self._game_engine.screen.get_rect()
        self.starfield_cfg = load_config_file('assets/cfg/starfield.json')

    def do_process_events(self, event: pygame.event):
        system_input(self.ecs_world, event, self.do_action)

    def simulate(self, delta_time):
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()

    def switch_scene(self, new_scene_name: str):
        self._game_engine.switch_scene(new_scene_name)

    def do_create(self):
        create_stars(self.ecs_world, self.starfield_cfg, self.screen)

    def do_update(self, delta_time: float):
        system_update_stars(self.ecs_world, delta_time, self.screen)

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)
        

    def do_action(self, action: CInputCommand):
        pass

    def do_clean(self):
        pass



