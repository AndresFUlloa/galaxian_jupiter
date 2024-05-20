import pygame

import esper
from src.ecs.components.c_input_command import CInputCommand


def create_debug_input(world: esper.World):
    switch_editor_mode = world.create_entity()
    world.add_component(
        switch_editor_mode,
        CInputCommand("TOGGLE_EDITOR", [pygame.K_TAB])
    )

    kill_all_action = world.create_entity()
    world.add_component(
        kill_all_action,
        CInputCommand("KILL_ALL", [pygame.K_k])
    )