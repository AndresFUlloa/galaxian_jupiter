import pygame
from src.create.prefab_creator_interface import TextAlignment
from src.create.prefab_creator_menu import add_menu_images, create_menu_texts
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_menu_state import CMenuState, MenuState
from src.ecs.systems.s_enemy_shooting import enemy_shooting_system
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_movement_text_menu import system_text_movement, system_text_end_movement
from src.engine.scenes.scene import Scene


class MenuScene(Scene):
    def __init__(self, engine: 'src.engine.game_engine') -> None:
        super().__init__(engine)
        self.screen = engine.screen
        self.window_cfg = engine.window_cfg
        self._accumulated_time = 0.0
        self.screen_size_height = engine.screen_size_height

    def do_create(self):
        super().do_create()
        create_menu_texts(self.ecs_world, self.screen_size_height)
        add_menu_images(self.ecs_world, self.screen_size_height)
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("PLAYER_SELECTION", [pygame.K_RETURN]))
        menu_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(menu_entity, CMenuState())
        self.c_menu_state = self.ecs_world.component_for_entity(menu_entity, CMenuState)

    def do_update(self, delta_time: float):
        super().do_update(delta_time)
        self._accumulated_time += delta_time
        if self.c_menu_state.state == MenuState.START:
            system_text_movement(self.ecs_world)
        system_movement(self.ecs_world, delta_time, False)
        

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_SELECTION":
            if c_input.phase == CommandPhase.START:
                if self.c_menu_state.state == MenuState.END:
                    self.switch_scene("LEVEL_01")
                elif self.c_menu_state.state == MenuState.START:
                    system_text_end_movement(self.ecs_world)
