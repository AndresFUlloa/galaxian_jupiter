
import pygame
from src.create.prefab_creator_interface import TextAlignment
from src.create.prefab_creator_menu import add_menu_images, create_menu_texts
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_movement import system_movement
from src.engine.scenes.scene import Scene


class MenuScene(Scene):
    def __init__(self,engine: 'src.engine.game_engine') -> None:
        super().__init__(engine)
        self.screen = engine.screen
        self.window_cfg = engine.window_cfg
        self._accumulated_time = 0.0
        self.screen_size_height = engine.screen_size_height


    def do_create(self):
       super().do_create()
       create_menu_texts(self.ecs_world,self.screen_size_height)
       add_menu_images(self.ecs_world)
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

            
                

