import esper, pygame
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.engine.service_locator import ServiceLocator
from src.ecs.systems.s_movement import system_movement
from src.ecs.components.tags.c_tag_ready_text import CTagReadyText
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator_interface import create_text, TextAlignment
from src.create.prefab_creator_play import create_enemies
from src.ecs.components.c_surface import CSurface


def system_update_play_state(world:esper.World, delta_time:float):
    c_p_s = world.get_component(CPlayState)[0][1]
    c_p_s.current_time += delta_time
    game_times_cfg = ServiceLocator.jsons_service.get('assets/cfg/game_times.json')
    system_movement(world, delta_time, c_p_s.state==PlayState.PAUSE)
    
    if c_p_s.state == PlayState.START:
        if c_p_s.current_time < game_times_cfg["ready_time_init"]:
            return
        if c_p_s.current_time >= game_times_cfg["ready_time_init"] and c_p_s.current_time < game_times_cfg["ready_time_enemy"]:
            if len(world.get_components(CTagReadyText)) == 0:
                ready_entity = create_text(world,"READY", 14, pygame.Color(234,61,1), pygame.Vector2(128, 200), TextAlignment.CENTER)
                world.add_component(ready_entity, CTagReadyText())           
            return
        if c_p_s.current_time >= game_times_cfg["ready_time_enemy"] and c_p_s.current_time < game_times_cfg["ready_time_off"]:
            if len(world.get_components(CTagEnemy)) == 0: 
                create_enemies(world, ServiceLocator.jsons_service.get("assets\cfg\enemies.json"))
            return
        if c_p_s.current_time >= game_times_cfg["ready_time_off"] and c_p_s.current_time < game_times_cfg["ready_time_player"]:
            ready_entity = world.get_component(CTagReadyText)[0][0]
            world.component_for_entity(ready_entity, CSurface).is_visible = False
            return