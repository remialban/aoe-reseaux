from core.buildings.archery_range import ArcheryRange
from core.buildings.barracks import Barracks
from core.buildings.camp import Camp
from core.buildings.farm import Farm
from core.buildings.house import House
from core.buildings.keep import Keep
from core.buildings.stable import Stable
from core.buildings.town_center import TownCenter
from core.resources_points.wood import Wood
from ui.gui.maps.big_map.sprites.buildings.house import HouseSprite
from ui.gui.maps.big_map.sprites.unit import UnitSprite
from ui.gui.utils.camera import Camera
from ui.gui.maps.big_map.sprites.grass import Grass
from ui.gui.maps.big_map.sprites.ressources.mine import MineSprite
from ui.gui.maps.big_map.sprites.buildings.archery_range import ArcheryRangeSprite
from ui.gui.maps.big_map.sprites.buildings.barracks import BarracksSprite
from ui.gui.maps.big_map.sprites.buildings.camp import CampSprite
from ui.gui.maps.big_map.sprites.buildings.farm import FarmSprite
from ui.gui.maps.big_map.sprites.buildings.keep import KeepSprite
from ui.gui.maps.big_map.sprites.buildings.stable import StableSprite
from ui.gui.maps.big_map.sprites.buildings.town_center import TownCenterSprite
from ui.gui.maps.big_map.sprites.ressources.wood import WoodSprite
from ui.gui.utils.isometry import Isometry
from ui.gui.maps.big_map.sprites.map import Map
from ui.ui_manager import UIManager


class BigMap(Map):
    def __init__(self, tile_length, offset_x, offset_y, screen):
        super().__init__(tile_length, 0, 0, Isometry(tile_length=Camera.get_tile_length), screen)
        for x in range(UIManager.get_game().get_map().get_width()):
            for y in range(UIManager.get_game().get_map().get_height()):
                self.grass_list.add(Grass(x, y))


    def add_resource_point_sprite(self, resource_point):
        match resource_point:
            case Wood():
                self.resource_points.add(WoodSprite(resource_point, self.isometry))
            case _:
                self.resource_points.add(MineSprite(resource_point, self.isometry))

    def add_building_sprite(self, building):
        match building:
            case TownCenter():
                self.buildings.add(TownCenterSprite(building))
            case ArcheryRange():
                self.buildings.add(ArcheryRangeSprite(building))
            case Barracks():
                self.buildings.add(BarracksSprite(building))
            case Camp():
                self.buildings.add(CampSprite(building))
            case House():
                self.buildings.add(HouseSprite(building))
            case Keep():
                self.buildings.add(KeepSprite(building))
            case Farm():
                self.buildings.add(FarmSprite(building))
            case Stable():
                self.buildings.add(StableSprite(building))
            case _:
                pass
        #self.buildings.add(TownCenterSprite(building))

    def add_unit_sprite(self, unit):
        self.units.add(UnitSprite(unit, self.isometry))