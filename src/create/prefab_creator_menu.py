

import pygame

import esper
from src.create.prefab_creator import create_sprite
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.tags.c_tag_movible import CTagMovible
from src.engine.service_locator import ServiceLocator


def create_menu_texts (world:esper.World,screen_size_height):
    text_entity = create_text(world, "1UP",8,pygame.Color(255, 50, 50),pygame.Vector2(50,10),TextAlignment.LEFT)
    world.add_component(text_entity, CTagMovible(50,10))

    text_entity =create_text(world, "HI-SCORE",8,pygame.Color(255, 50, 50),pygame.Vector2(100,10),TextAlignment.LEFT)
    world.add_component(text_entity, CTagMovible(100,10))
    
    text_entity =create_text(world, "00",8,pygame.Color(255, 255, 255),pygame.Vector2(65,20),TextAlignment.LEFT)
    world.add_component(text_entity, CTagMovible(65,20))
    
    text_entity =create_text(world, "JUPITER GALAXIAN",8,pygame.Color(255, 255, 255),pygame.Vector2(120,80),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,80))
    
    text_entity =create_text(world, "1 PLAYER",8,pygame.Color(180, 119, 252),pygame.Vector2(120,108),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,108))
    
    #create_text(world, "►",8,pygame.Color(255, 255, 255),pygame.Vector2(80,108),TextAlignment.LEFT)
    text_entity =create_text(world, "NAMCOT",8,pygame.Color(255, 50, 50),pygame.Vector2(120,178),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,178))
    
    text_entity =text_entity =create_text(world, "©1979  1984 NAMCO LTD.",8,pygame.Color(255, 255, 255),pygame.Vector2(120,198),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,198))
    create_text(world, "ALL RIGHTS RESERVED",8,pygame.Color(255, 255, 255),pygame.Vector2(120,208),TextAlignment.CENTER)
    world.add_component(text_entity, CTagMovible(120,208))

def add_menu_images(world:esper.World):
    arrow_surface = ServiceLocator.images_service.get('assets/img/triangulo-blanco.png')
    pos = pygame.Vector2(80,109)
    vel = pygame.Vector2(0, 0)
    arrow_entity = create_sprite(world, pos, vel, arrow_surface, None)
    world.add_component(arrow_entity,CTagMovible(120,208))

 


