import pygame
import esper
import random
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator

def create_square(world:esper.World, size:pygame.Vector2, pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity, 
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface, animations: dict = None) -> int:
    sprite_entity = world.create_entity()
    c_s = CSurface.from_surface(surface)
    if animations is not None:
        c_s.area.width = c_s.area.width / animations['number_frames']
        world.add_component(sprite_entity, CAnimation(animations))

    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    world.add_component(sprite_entity, c_s)
    return sprite_entity


def create_player(world: esper.World, player_info: dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_info['image'])
    player_size = player_surface.get_size()
    position = pygame.Vector2(
        player_info['start_pos']['x'] - player_size[0]/2, player_info['start_pos']['y'] - player_size[1])
    velocity = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, position, velocity, player_surface)
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    world.add_component(input_left, CInputCommand("PLAYER_LEFT", [pygame.K_LEFT, pygame.K_a]))
    world.add_component(input_right, CInputCommand("PLAYER_RIGHT", [pygame.K_RIGHT, pygame.K_d]))



def create_stars(world: esper.World, stars_info: dict, screen:pygame.Surface) -> None:
    star_colors = stars_info["star_colors"]
    number_of_stars = stars_info["number_of_stars"]
    vertical_speed = stars_info["vertical_speed"]
    blink_rate = stars_info["blink_rate"]
    
    for i in range(number_of_stars):
        pos = pygame.Vector2(random.randint(0, screen.get_width()-1), random.randint(0,screen.get_height()-1))
        vel = pygame.Vector2(0, random.randint(vertical_speed["min"], vertical_speed["max"]))
        dict_color = star_colors[random.randint(0, len(star_colors)-1)]
        color = pygame.Color(dict_color["r"], dict_color["g"], dict_color["b"])
        blink_time = random.uniform(blink_rate["min"], blink_rate["max"])
        star_entity = create_square(world, pygame.Vector2(1,1), pos, vel, color)
        world.add_component(star_entity, CTagStar(blink_time, random.choice([True, False])))



   