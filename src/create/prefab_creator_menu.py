

import pygame

import esper
from src.create.prefab_creator import create_sprite
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.tags.c_tag_movible import CTagMovible
from src.engine.service_locator import ServiceLocator


def create_menu_texts (world:esper.World,screen_size_height):
    pos_y= screen_size_height+10
    text_entity = create_text(world, "1UP",8,pygame.Color(255, 50, 50),pygame.Vector2(50,pos_y),TextAlignment.LEFT)
    world.add_component(text_entity, CTagMovible(50,10))
    
    pos_y= screen_size_height+10
    text_entity =create_text(world, "HI-SCORE",8,pygame.Color(255, 50, 50),pygame.Vector2(100,pos_y),TextAlignment.LEFT)
    world.add_component(text_entity, CTagMovible(100,10))

    pos_y= screen_size_height+20
    text_entity =create_text(world, "00",8,pygame.Color(255, 255, 255),pygame.Vector2(65,pos_y),TextAlignment.LEFT)
    world.add_component(text_entity, CTagMovible(65,20))
    
    pos_y= screen_size_height+80
    text_entity =create_text(world, "JUPITER GALAXIAN",8,pygame.Color(255, 255, 255),pygame.Vector2(120,pos_y),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,80))
    
    pos_y= screen_size_height+108
    text_entity =create_text(world, "1 PLAYER",8,pygame.Color(180, 119, 252),pygame.Vector2(120,pos_y),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,108))
    
    #create_text(world, "►",8,pygame.Color(255, 255, 255),pygame.Vector2(80,108),TextAlignment.LEFT)
    pos_y= screen_size_height+178
    text_entity =create_text(world, "NAMCOT",8,pygame.Color(255, 50, 50),pygame.Vector2(120,pos_y),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,178))
    
    pos_y= screen_size_height+198
    text_entity =create_text(world, "©1979  1984 NAMCO LTD.",8,pygame.Color(255, 255, 255),pygame.Vector2(120,pos_y),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,198))
    
    pos_y= screen_size_height+208
    text_entity =create_text(world, "ALL RIGHTS RESERVED",8,pygame.Color(255, 255, 255),pygame.Vector2(120,pos_y),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,208))

def add_menu_images(world:esper.World,screen_size_height):
    arrow_surface = ServiceLocator.images_service.get('assets/img/triangulo-blanco.png')
    pos_y= screen_size_height+109
    pos = pygame.Vector2(80,pos_y)
    vel = pygame.Vector2(0, 0)
    arrow_entity = create_sprite(world, pos, vel, arrow_surface, None)
    world.add_component(arrow_entity,CTagMovible(120,109))

 


