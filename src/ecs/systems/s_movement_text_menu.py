import esper
from src.ecs.components.c_menu_state import CMenuState, MenuState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_movible import CTagMovible


def system_text_movement(world: esper.World):
    moving_texts = world.get_components(CTransform, CTagMovible)
    ended = True
    for text, (c_t, c_t_m) in moving_texts:
        if c_t_m.dest_y < c_t.pos.y:
            c_t.pos.y -= 1
            ended = False

    if ended:
        world.get_component(CMenuState)[0][1].state = MenuState.END


def system_text_end_movement(world: esper.World):
    moving_texts = world.get_components(CTransform, CTagMovible)
    for _, (c_t, c_t_m) in moving_texts:
        c_t.pos.y = c_t_m.dest_y

    world.get_component(CMenuState)[0][1].state = MenuState.END
