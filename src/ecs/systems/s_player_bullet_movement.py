
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_bullet_state import CBulletState, BulletState
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_velocity import CVelocity


def system_player_bullet_movement(world: esper.World, c_input: CInputCommand, input_velocity: int, player_entity: int):
    if c_input.name not in ["PLAYER_LEFT", "PLAYER_RIGHT"]:
        return

    direction = 1 if c_input.name == "PLAYER_RIGHT" else -1
    c_v_p = world.component_for_entity(player_entity, CVelocity)
    bullet_entity = _search_charged_bullet(world)
    c_v_b = world.component_for_entity(bullet_entity, CVelocity) if bullet_entity is not None else None

    if c_input.phase == CommandPhase.START:
        c_v_p.vel.x += direction * input_velocity
        _update_bullet_velocity(c_v_b, direction * input_velocity)
    elif c_input.phase == CommandPhase.END:
        c_v_p.vel.x -= direction * input_velocity
        _update_bullet_velocity(c_v_b, -direction * input_velocity)


def _search_charged_bullet(world: esper.World):
    components = world.get_components(CBulletState, CTagPlayerBullet)
    for bullet_entity, (c_b_s, _) in components:
        if c_b_s.state == BulletState.IDLE:
            return bullet_entity
    return None


def _update_bullet_velocity(c_v_b: CVelocity, velocity_change: int):
    if c_v_b is not None:
        c_v_b.vel.x += velocity_change
