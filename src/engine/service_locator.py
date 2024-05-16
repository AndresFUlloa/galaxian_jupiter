from src.engine.services.fonts_service import FontsService
from src.engine.services.image_service import ImagesService
from src.engine.services.jsons_service import JsonsService
from src.engine.services.sounds_service import SoundsService


class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
    fonts_service = FontsService()
    jsons_service = JsonsService()
