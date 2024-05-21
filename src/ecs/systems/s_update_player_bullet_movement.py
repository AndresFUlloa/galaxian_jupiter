import esper
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_player_bullet_movement import _search_charged_bullet


def system_update_player_bullet_movement(world: esper.World, player_entity: int, player_velocity: int):
    c_t_p = world.component_for_entity(player_entity, CTagPlayer)
    c_v_p = world.component_for_entity(player_entity, CVelocity)
    bullet_entity = _search_charged_bullet(world)

    if c_t_p.right == c_t_p.left:
        c_v_p.vel.x = 0
        if bullet_entity is not None:
            world.component_for_entity(bullet_entity, CVelocity).vel.x = 0
        return

    if c_t_p.right:
        c_v_p.vel.x = player_velocity
        if bullet_entity is not None:
            world.component_for_entity(bullet_entity, CVelocity).vel.x = player_velocity

    if c_t_p.left:
        c_v_p.vel.x = -1 * player_velocity
        if bullet_entity is not None:
            world.component_for_entity(bullet_entity, CVelocity).vel.x = -1 * player_velocity
