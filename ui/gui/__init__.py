from math import radians, cos

import pygame

from ui import UI
from ui.gui.maps.minimap.mini_map import MiniMap
from ui.gui.screen_manager import ScreenManager, Screens
from ui.gui.screens.map import MapScreen
from ui.gui.utils.camera import Camera
from ui.gui.maps.big_map.big_map import BigMap


# Launch a pygame window
# class GUI(UI):
#     # Setup pygame
#     def setup(self):
#         #setup pygame
#         pygame.init()
#         pygame.font.init()
#         pygame.mixer.init()
#
#         #set the screen size
#         info = pygame.display.Info()
#         screen_width, screen_height = info.current_w, info.current_h
#         self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
#         #set the window title
#         pygame.display.set_caption("AIge of EmpAIres - Groupe 1")
#         #set the clock
#         self.clock = pygame.time.Clock()
#
#
#         self.map = BigMap(50, -screen_width / 2, 0, self.screen)
#         self.minimap = MiniMap(None, screen_width, 0, self.screen)
#
#         # for resource in UIManager.get_game().get_map().get_resources():
#         #     self.map.add_resource_point(resource)
#         #
#         # for building in UIManager.get_game().get_map().get_buildings():
#         #     self.map.add_building(building)
#         #
#         # for unit in UIManager.get_game().get_map().get_units():
#         #     self.map.add_units(unit)
#         #
#         # for building in UIManager.get_game().get_map().get_buildings():
#         #     self.minimap.add_building(building)
#
#
#     def loop(self):
#         #run the game loop
#         running = True
#         while running:
#             #check for events
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                     UIManager.stop()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_F12:
#                         UIManager.change_ui(UIList.CLI)
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     coordinates = list(pygame.mouse.get_pos())
#                     coordinates = list(event.pos)
#                     #coordinates[0] += self.screen.get_rect().x
#                     coef_mul = self.map.isometry.get_tile_length() / self.minimap.isometry.get_tile_length()
#                     new_x = (coordinates[0] - self.screen.get_width() + cos(radians(30)) * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width())*coef_mul #*cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
#                     new_x -= self.screen.get_width() /2
#
#                     new_y = (coordinates[1] - self.screen.get_height() + cos(radians(60)) * self.minimap.isometry.get_tile_length() * (UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height()))*coef_mul #*cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
#                     new_y -= self.screen.get_height() /2
#                     new_y -= 2*cos(radians(60)) * self.map.isometry.get_tile_length()
#                     print(new_x)
#                     Camera.set_camera(new_x, new_y)
#             if pygame.mouse.get_pressed()[0]:
#                 coordinates = list(pygame.mouse.get_pos())
#                 #coordinates = list(event.pos)
#                 # coordinates[0] += self.screen.get_rect().x
#                 coef_mul = self.map.isometry.get_tile_length() / self.minimap.isometry.get_tile_length()
#                 new_x = (coordinates[0] - self.screen.get_width() + cos(radians(30))
#                          * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()) * coef_mul
#                 new_x -= self.screen.get_width() / 2
#
#                 new_y = (coordinates[1] - self.screen.get_height() + cos(
#                     radians(60)) * self.minimap.isometry.get_tile_length() * (
#                                      UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height())) * coef_mul  # *cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
#                 new_y -= self.screen.get_height() / 2
#                 new_y -= 2 * cos(radians(60)) * self.map.isometry.get_tile_length()
#                 Camera.set_camera(new_x, new_y)
#             self.screen.fill((61, 10, 7))
#
#             offset = 5
#             if pygame.key.get_pressed()[pygame.K_r]:
#                 game = UIManager.get_game().get_map()
#                 buildings = list(game.get_buildings())[0]
#                 UIManager.get_game().get_map().remove_building(buildings)
#
#
#             if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_q]:
#                 Camera.add_x(-offset)
#             if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
#                 Camera.add_x(offset)
#             if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_z]:
#                 Camera.add_y(-offset)
#             if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
#                 Camera.add_y(offset)
#
#
#             offset = 20
#             if (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_q]) and (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
#                 Camera.add_x(-offset)
#             if (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]) and (pygame.key.get_pressed()[pygame.K_LSHIFT]  or pygame.key.get_pressed()[pygame.K_RSHIFT]):
#                 Camera.add_x(offset)
#             if (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_z]) and (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
#                 Camera.add_y(-offset)
#             if (pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]) and (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
#                 Camera.add_y(offset)
#
#             if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
#                 Camera.zoom_in()
#             if pygame.key.get_pressed()[pygame.K_KP_MINUS]:
#                 Camera.zoom_out()
#
#             #clear the screen
#
#             for resource in UIManager.get_game().get_map().get_resources() - self.map.resource_points_objects:
#                 self.map.add_resource_point(resource)
#                 self.minimap.add_resource_point(resource)
#             for building in UIManager.get_game().get_map().get_buildings() - self.map.buildings_objects:
#                 self.map.add_building(building)
#                 self.minimap.add_building(building)
#             for unit in UIManager.get_game().get_map().get_units() - self.map.units_objects:
#                 self.map.add_units(unit)
#                 self.minimap.add_units(unit)
#
#             for resource in self.map.resource_points_objects - UIManager.get_game().get_map().get_resources():
#                 self.map.remove_resource_point(resource)
#                 self.minimap.remove_resource_point(resource)
#             for building in self.map.buildings_objects - UIManager.get_game().get_map().get_buildings():
#                 self.map.remove_building(building)
#                 self.minimap.remove_building(building)
#             for unit in self.map.units_objects - UIManager.get_game().get_map().get_units():
#                 self.map.remove_unit(unit)
#                 self.minimap.remove_unit(unit)
#
#             self.map.update()
#             self.map.draw()
#
#             self.minimap.update()
#             self.minimap.draw()
#             coef = self.map.isometry.get_tile_length() / self.minimap.isometry.get_tile_length()
#
#             rect = pygame.rect.Rect(0, 0, self.screen.get_width()/coef, self.screen.get_height()/coef)
#
#             new_x = (Camera.get_x() + self.screen.get_width() / 2) #- cos(radians(30)) * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
#             new_x /= coef
#             new_x -= ( - self.screen.get_width() + cos(radians(30)) * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width())
#
#             new_y = (Camera.get_y())
#             new_y += 2*cos(radians(60)) * self.map.isometry.get_tile_length()
#             new_y += self.screen.get_height() / 2
#             new_y /= coef
#             new_y -= - self.screen.get_height() + cos(
#                 radians(60)) * self.minimap.isometry.get_tile_length() * (
#                                  UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height())
#
#             # new_y = (coordinates[1] - self.screen.get_height() + cos(
#             #     radians(60)) * self.minimap.isometry.get_tile_length() * (
#             #                  UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height())) * coef_mul  # *cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
#             # new_y -= self.screen.get_height() / 2
#             # new_y -= 2 * cos(radians(60)) * self.map.isometry.get_tile_length()
#
#             rect.center = new_x, new_y
#             #pygame.draw.rect(self.screen, (255, 0, 0), (new_x, new_y, self.screen.get_width()/coef, self.screen.get_height()/coef), 2)
#             pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
#
#             pygame.display.flip()
#
#             #tick the clock
#             self.clock.tick(60)
#             UIManager.get_game().party()
#
#     def cleanup(self):
#         pygame.quit()

class GUI(UI):
    def setup(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        #set the screen size
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        #set the window title
        pygame.display.set_caption("AIge of EmpAIres - Groupe 1")
        #set the clock
        self.clock = pygame.time.Clock()

        ScreenManager.add_screen(Screens.MAP, MapScreen(self.screen))
        ScreenManager.change_screen(Screens.MAP)


    def loop(self):
        ScreenManager.loop()

    def cleanup(self):
        pygame.quit()
