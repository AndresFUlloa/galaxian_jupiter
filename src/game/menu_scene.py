import pygame
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_movement import system_movement
from src.engine.scenes.scene import Scene


class MenuScene(Scene):
    def __init__(self, engine: 'src.engine.game_engine') -> None:
        super().__init__(engine)
        self.screen = engine.screen
        self.window_cfg = engine.window_cfg
        self._accumulated_time = 0.0

    def do_create(self):
        super().do_create()
        create_text(self.ecs_world, "1UP", 6, pygame.Color(255, 50, 50), pygame.Vector2(50, 10), TextAlignment.LEFT)
        create_text(self.ecs_world, "HI-SCORE", 6, pygame.Color(255, 50, 50), pygame.Vector2(100, 10),
                    TextAlignment.LEFT)
        create_text(self.ecs_world, "00", 6, pygame.Color(255, 255, 255), pygame.Vector2(65, 20), TextAlignment.LEFT)
        create_text(self.ecs_world, "JUPITER GALAXIAN", 6, pygame.Color(255, 255, 255), pygame.Vector2(120, 80),
                    TextAlignment.CENTER)
        create_text(self.ecs_world, "1 PLAYER", 6, pygame.Color(180, 119, 252), pygame.Vector2(120, 108),
                    TextAlignment.CENTER)
        create_text(self.ecs_world, "►", 5, pygame.Color(255, 255, 255), pygame.Vector2(80, 108), TextAlignment.LEFT)
        create_text(self.ecs_world, "NAMCOT", 6, pygame.Color(255, 50, 50), pygame.Vector2(120, 178),
                    TextAlignment.CENTER)
        create_text(self.ecs_world, "©1979  1984 NAMCO LTD.", 6, pygame.Color(255, 255, 255), pygame.Vector2(120, 198),
                    TextAlignment.CENTER)
        create_text(self.ecs_world, "ALL RIGHTS RESERVED", 6, pygame.Color(255, 255, 255), pygame.Vector2(120, 208),
                    TextAlignment.CENTER)
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("PLAYER_SELECTION", [pygame.K_RETURN]))

    def do_update(self, delta_time: float):
        super().do_update(delta_time)
        self._accumulated_time += delta_time
        system_movement(self.ecs_world, delta_time, False)


    def do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_SELECTION":
            if c_input.phase == CommandPhase.START:
                # change scene
                self.switch_scene("LEVEL_01")
