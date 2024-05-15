import esper
from src.ecs.components.c_bullet_state import CBulletState, BulletState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.s_player_boundaries import _get_num_charged_bullets 


def system_shoot_bullet(world: esper.World, num_bullets, bullet_entity: int, bullet_speed: int) -> bool:
    
    if bullet_entity is None or _get_num_charged_bullets(world) <= 0:
        return False

    c_v = world.component_for_entity(bullet_entity, CVelocity)
    c_v.vel.x = 0
    c_v.vel.y = -bullet_speed

    c_b_s = world.component_for_entity(bullet_entity, CBulletState)
    c_b_s.state = BulletState.SHOT
    return True
