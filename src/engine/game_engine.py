import esper
import pygame

from src.create.prefab_creator import create_player, create_input_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
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
        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        if not self.pause:
            self.clock.tick(self.frame_rate)
            self.delta_time = self.clock.get_time() / 1000.0
            self.current_time += self.delta_time
        else:
            self.clock.tick(0)
            self.delta_time = 0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
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