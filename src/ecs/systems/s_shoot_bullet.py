import esper
from src.ecs.components.c_bullet_state import CBulletState, BulletState
from src.ecs.components.c_velocity import CVelocity

from src.ecs.systems.s_player_bullet_movement import _search_charged_bullet
from src.engine.service_locator import ServiceLocator


def system_shoot_bullet(world: esper.World, bullet_speed: int) -> bool:

    bullet_entity = _search_charged_bullet(world)

    if bullet_entity is None:
        return False

    c_v = world.component_for_entity(bullet_entity, CVelocity)
    c_v.vel.x = 0
    c_v.vel.y = -bullet_speed

    c_b_s = world.component_for_entity(bullet_entity, CBulletState)

    c_b_s.state = BulletState.SHOT
    ServiceLocator.sounds_service.play("assets/snd/player_shoot.ogg")
    return True

