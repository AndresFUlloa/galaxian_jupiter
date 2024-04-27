import esper
import pygame

from src.create.prefab_creator import create_player
from src.ecs.systems.s_rendering import system_rendering
from src.utilities.config_loader import load_config_file


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()
        screen_size = self.window_cfg['size']
        t_color = self.window_cfg["bg_color"]
        pygame.init()
        pygame.display.set_caption(self.window_cfg['title'])
        self.screen = pygame.display.set_mode((screen_size['w'], screen_size['h']), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.frame_rate = self.window_cfg['framerate']
        self.delta_time = 0
        self.current_time = 0.0
        self.ecs_world = esper.World()
        self.bg_color = pygame.Color(t_color['r'], t_color['g'], t_color['b'])
        self.pause = False

    def _load_config_files(self):
        self.interface_cfg = load_config_file('assets/cfg/interface.json')
        self.starfield_cfg = load_config_file('assets/cfg/starfield.json')
        self.window_cfg = load_config_file('assets/cfg/window.json')
        self.player_cfg = load_config_file('assets/cfg/player.json')

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        create_player(self.ecs_world, self.player_cfg)

    def _calculate_time(self):
        if not self.pause:
            self.clock.tick(self.frame_rate)
            self.delta_time = self.clock.get_time() / 1000.0
            self.current_time += self.delta_time
        else:
            self.clock.tick(0)
            self.delta_time = 0

    def _process_events(self):
        pass

    def _update(self):
        pass

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
