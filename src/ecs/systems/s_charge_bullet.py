import esper
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.create.prefab_creator_play import create_player_bullet
from src.ecs.components.c_bullet_state import CBulletState, BulletState

def system_charge_bullet(world:esper.World, bullet_info:dict, player_entity:int):
    components = world.get_components(CTagPlayerBullet, CBulletState)

    if len(components) <= 0:
        return create_player_bullet(world, bullet_info, player_entity)

    for bullet_entity, (_, c_b_s) in components:
        if c_b_s.state == BulletState.IDLE:
            return bullet_entity
    return None