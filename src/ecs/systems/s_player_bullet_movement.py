import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_bullet_state import CBulletState, BulletState
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_play_state import CPlayState, PlayState


def system_player_bullet_movement(world: esper.World, c_input: CInputCommand, player_entity: int):
    if c_input.name not in ["PLAYER_LEFT", "PLAYER_RIGHT"]:
        return

    c_t_p = world.component_for_entity(player_entity, CTagPlayer)
    if world.get_component(CPlayState)[0][1].state != PlayState.PLAY:
        return

    if c_input.phase == CommandPhase.START:
        if c_input.name == "PLAYER_RIGHT":
            c_t_p.right = True
        else:
            c_t_p.left = True
    elif c_input.phase == CommandPhase.END:
        if c_input.name == "PLAYER_RIGHT":
            c_t_p.right = False
        else:
            c_t_p.left = False


def _search_charged_bullet(world: esper.World):
    components = world.get_components(CBulletState, CTagPlayerBullet)
    for bullet_entity, (c_b_s, _) in components:
        if c_b_s.state == BulletState.IDLE:
            return bullet_entity
    return None


def _update_bullet_velocity(c_v_b: CVelocity, velocity_change: int):
    if c_v_b is not None:
        c_v_b.vel.x += velocity_change
