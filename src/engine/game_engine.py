import esper
import pygame

from src.create.prefab_creator import create_player, create_input_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_boundaries import system_player_boundaries
from src.ecs.systems.s_rendering import system_rendering
from src.engine.scenes.scene import Scene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene
from src.utilities.config_loader import load_config_file


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()
        screen_size = self.window_cfg['size']
        t_color = self.window_cfg["bg_color"]
        pygame.init()
        pygame.display.set_caption(self.window_cfg['title'])
        self.screen = pygame.display.set_mode((screen_size['w'], screen_size['h']), pygame.SCALED) #eliminar el scaled
        self._clock = pygame.time.Clock()
        self.is_running = False
        self._framerate = self.window_cfg['framerate']
        self._delta_time = 0
        self.current_time = 0.0
        self.ecs_world = esper.World()
        self.bg_color = pygame.Color(t_color['r'], t_color['g'], t_color['b'])

        self._scenes: dict[str, Scene] = {"LEVEL_01": PlayScene("assets/cfg/lvls.json", self)}
        self._scenes["MENU"] = MenuScene(self)
        
        self._current_scene: Scene = None
        self._scene_name_to_switch: str = None

    def _load_config_files(self):
        self.interface_cfg = load_config_file('assets/cfg/interface.json')
        self.window_cfg = load_config_file('assets/cfg/window.json')
        self.player_cfg = load_config_file('assets/cfg/player.json')


    def run(self, star_scene_name: str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[star_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
        self._clean()

    def switch_scene(self, new_scene_name: str):
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self._clock.tick(self._framerate)
        self._delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self._delta_time)

    def _draw(self):
        self.screen.fill(self.bg_color)
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action: CInputCommand):
        self._current_scene.do_action(action)
