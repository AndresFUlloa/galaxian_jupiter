import esper, pygame, random
from src.ecs.components.c_enemies_stop_motion import CEnemiesStopMotion
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemies_movement(world: esper.World, screen: pygame.Surface, delta_time: float, time_to_stop: dict,
                            stopped_time: dict, margin: int):
    c_e_s_m = world.get_component(CEnemiesStopMotion)[0][1]

    if not c_e_s_m.stopped:
        c_e_s_m.remaining_time_to_stop -= delta_time
        if c_e_s_m.remaining_time_to_stop <= 0:
            c_e_s_m.stopped = True
            _change_enemies_velocity(world, 0)
            c_e_s_m.time_to_stop = random.uniform(time_to_stop['min'], time_to_stop['max'])
            c_e_s_m.remaining_time_to_stop = c_e_s_m.time_to_stop

    else:
        c_e_s_m.remaining_stopped_time -= delta_time
        if c_e_s_m.remaining_stopped_time <= 0:
            c_e_s_m.stopped = False
            c_e_s_m.stopped_time = random.uniform(stopped_time['min'], stopped_time['max'])
            c_e_s_m.remaining_stopped_time = c_e_s_m.time_to_stop
            _change_enemies_velocity(world, c_e_s_m.prev_velocity)

    if not c_e_s_m.stopped:
        components = world.get_components(CTransform, CSurface, CVelocity, CTagEnemy)
        vel: int = None
        for enemy_entity, (c_t, c_s, c_v, _) in components:
            rect = c_s.area.copy()
            rect.topleft = c_t.pos
            if rect.right > screen.get_width() - margin or c_t.pos.x < margin:
                vel = c_v.vel.x * -1
                break

        if vel is not None:
            _change_enemies_velocity(world, vel)
            c_e_s_m.prev_velocity = vel


def _change_enemies_velocity(world: esper.World, velocity: float):
    components = world.get_components(CVelocity, CEnemyState, CTagEnemy)

    c_v: CVelocity
    c_e_s: CEnemyState
    for enemy_entity, (c_v, c_e_s, _) in components:
        c_v.vel.x = velocity
        if velocity == 0:
            c_e_s.state = EnemyState.IDLE
        else:
            c_e_s.state = EnemyState.MOVE
