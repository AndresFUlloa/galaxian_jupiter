import random
import esper
from src.create.prefab_creator_play import create_enemy_bullet
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def enemy_shooting_system(world:esper.World,acumulated_time: float,bullet_info:dict):
    #determinar el tiempo de disparo
    interval = 5
    # si se cumple el intervalo haga que un enemigo dispare 
    if not int(acumulated_time / interval) % 2 ==0:
        components  = world.get_components(CTransform,CTagEnemy)
        number_of_enemys = len(components)
        if(number_of_enemys>0):
        # seleccionar al azar un enemigo
            enemy_index = random.randrange(0,number_of_enemys,1)
            enemy_entity = components[0][0]
            create_enemy_bullet(world,bullet_info,enemy_entity)

            
            
            


    