import esper
from src.create.prefab_creator_play import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def system_collision_bullet_enemy(world: esper.World, exp_info: dict):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagPlayerBullet)

    for bullet_entity, (b_s, b_t, _,) in bullet_components:
        pl_rect = CSurface.get_area_relative(b_s.area, b_t.pos)
        for enemy_entity, (c_s, c_t, _) in components:
            ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
            if ene_rect.colliderect(pl_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_t.pos, exp_info)
