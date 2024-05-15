


import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_movible import CTagMovible


def system_text_movement(world:esper.World):
    moving_texts  = world.get_components(CTransform,CTagMovible)
    for text,(c_t,c_t_m) in moving_texts:
        if c_t.pos.y<=c_t_m.dest_y: 
           c_t.pos.y -=1
      

