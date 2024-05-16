import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar


def system_movement(world: esper.World, delta_time: float, paused: bool):
    components = world.get_components(CVelocity, CTransform)

    c_v: CVelocity
    c_t: CTransform
    for entity, (c_v, c_t) in components:
        if not paused or world.has_component(entity, CTagStar):
            c_t.pos.x += c_v.vel.x * delta_time
            c_t.pos.y += c_v.vel.y * delta_time