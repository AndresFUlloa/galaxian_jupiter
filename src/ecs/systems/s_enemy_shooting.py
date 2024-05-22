import random
import esper

from src.create.prefab_creator_play import create_enemy_bullet
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_emeny_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def system_enemy_shooting(world: esper.World, acumulated_time: float, bullet_info: dict, shoot_time: dict):
    # determinar el tiempo de disparo
    interval = random.uniform(shoot_time['min'], shoot_time['max'])
    # si se cumple el intervalo haga que un enemigo dispare
    bala = world.get_component(CTagEnemyBullet)

    if (not (int(acumulated_time / interval) % 2 == 0)) and len(bala) == 0:
        components = world.get_components(CTransform, CTagEnemy)
        player = world.get_component(CTagPlayer)[0][0]
        number_of_enemys = len(components)
        if (number_of_enemys > 0):
            # seleccionar al azar un enemigo
            enemy_index = random.randrange(0, number_of_enemys, 1)
            enemy_entity = components[enemy_index][0]
            # disparar
            ServiceLocator.sounds_service.play("assets/snd/player_shoot.ogg")
            create_enemy_bullet(world, bullet_info, enemy_entity, player)
