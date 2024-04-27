import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement(world: esper.World, delta_time: float):
    components = world.get_components(CVelocity, CTransform)

    c_v: CVelocity
    c_t: CTransform

    for entity, (c_v, c_t) in components:
            c_t.pos.x += c_v.vel.x * delta_time
            c_t.pos.y += c_v.vel.y * delta_time
