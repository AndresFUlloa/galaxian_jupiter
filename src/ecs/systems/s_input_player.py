from typing import Callable

import pygame

import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input_player(world: esper.World,
                        event: pygame.Event,
                        do_action: Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)
    c_input: CInputCommand
    for _, c_input in components:
        if event.type == pygame.KEYDOWN and event.key in c_input.keys:
            c_input.phase = CommandPhase.START
            do_action(c_input)
        elif event.type == pygame.KEYUP and event.key in c_input.keys:
            c_input.phase = CommandPhase.END
            do_action(c_input)
