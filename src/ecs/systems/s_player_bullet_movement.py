
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_bullet_state import CBulletState, BulletState
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_velocity import CVelocity


def system_player_bullet_movement(world:esper.World, c_input:CInputCommand, input_velocity:int, player_entity:int):
    bullet_entity = _search_charged_bullet(world)

    if c_input.name == "PLAYER_LEFT":
        c_v_p = world.component_for_entity(player_entity, CVelocity)
        c_v_b: CVelocity = None
        if bullet_entity is not None:
             c_v_b = world.component_for_entity(bullet_entity, CVelocity)
             _update_bullet_velocity(c_v_b, c_input.phase, c_input.name, input_velocity)
        if c_input.phase == CommandPhase.START:
            c_v_p.vel.x += input_velocity
            _update_bullet_velocity(c_v_b, c_input.phase, c_input.name, input_velocity)
        elif c_input.phase == CommandPhase.END:
            c_v_p.vel.x -= input_velocity
            _update_bullet_velocity(c_v_b, c_input.phase, c_input.name, input_velocity)
    if c_input.name == "PLAYER_RIGHT":
        c_v_p = world.component_for_entity(bullet_entity, CVelocity)
        c_v_b: CVelocity = None
        if bullet_entity is not None:
             c_v_b = world.component_for_entity(bullet_entity, CVelocity)
        if c_input.phase == CommandPhase.START:
            c_v_p.vel.x -= input_velocity
            _update_bullet_velocity(c_v_b, c_input.phase, c_input.name, input_velocity)
        elif c_input.phase == CommandPhase.END:
            c_v_p.vel.x += input_velocity
            _update_bullet_velocity(c_v_b, c_input.phase, c_input.name, input_velocity)

def _search_charged_bullet(world:esper.World):
    components = world.get_components(CBulletState, CTagPlayerBullet)

    for bullet_entity, (c_b_s, _) in components:
        if c_b_s.state == BulletState.IDLE:
            return bullet_entity
    return None

def _update_bullet_velocity(c_v_b:CVelocity, phase:CommandPhase, c_input_name:str, input_velocity:int):
    if c_v_b is None:
        return
    if c_input_name == "PLAYER_LEFT":
        if phase == CommandPhase.START:
            c_v_b.vel.x += input_velocity
        elif phase == CommandPhase.END:
            c_v_b.vel.x -= input_velocity
    if c_input_name == "PLAYER_RIGHT":
        if phase == CommandPhase.START:
            c_v_b.vel.x -= input_velocity
        elif phase == CommandPhase.END:
            c_v_b.vel.x += input_velocity