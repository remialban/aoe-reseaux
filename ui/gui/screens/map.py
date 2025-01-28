from math import cos, radians

import pygame

from ui.enums import UIList
from ui.gui.maps.minimap.mini_map import MiniMap
from ui.gui.utils.camera import Camera


from ui.gui.maps.big_map.big_map import BigMap
from ui.gui.screens import Screen
from ui.ui_manager import UIManager

from tkinter import *
from tkinter import messagebox


class MapScreen(Screen):
    def __init__(self, window):
        super().__init__(window)

    def setup(self):
        self.map = BigMap(50, 0, 0, self._window)

        self.clock = pygame.time.Clock()

        screen_width, screen_height = self._window.get_size()
        self.map = BigMap(50, -screen_width / 2, 0, self._window)
        self.minimap = MiniMap(None, screen_width, 0, self._window)
        self.screen = self._window

        self.resources_showed = False

        self.position_rect = None
        self.correct_position = False

    # def check_position(self, x, y):
    #     if self.position_rect is None:
    #         return True
    #
    #     if self.position_rect.midleft[0] < self.screen.get_width()-self.minimap.minimap_width and
    def loop(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                UIManager.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F9:
                    UIManager.change_ui(UIList.CLI)
                if event.key == pygame.K_TAB:
                    UIManager.get_game().pause()
                    UIManager.render_html()
                    UIManager.open_in_browser()
                if event.key == pygame.K_p:
                    UIManager.get_game().pause()
                if event.key == pygame.K_r:
                    UIManager.get_game().resume()
                if event.key == pygame.K_F11:
                    backup_name = UIManager.get_name()
                    UIManager.save_game(backup_name)
                    win = Tk()  # to hide the main window
                    win.wm_withdraw()
                    messagebox.showinfo(
                        "Sauvegarde réussie!",
                        'La partie a bien été enregistré avec le nom "'
                        + backup_name
                        + '"',
                    )
                    # stop tkinter
                    win.destroy()

                if event.key == pygame.K_F1:
                    self.resources_showed = not self.resources_showed

            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinates = list(pygame.mouse.get_pos())
                coordinates = list(event.pos)
                x, y = coordinates

                # if x >= self.screen.get_width()-self.minimap.minimap_width or y >= self.screen.get_height() - self.minimap.minimap_height:
                #     #coordinates[0] += self.screen.get_rect().x
                #     coef_mul = self.map.isometry.get_tile_length() / self.minimap.isometry.get_tile_length()
                #     new_x = (coordinates[0] - self.screen.get_width() + cos(radians(30)) * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width())*coef_mul #*cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
                #     new_x -= self.screen.get_width() /2
                #
                #     new_y = (coordinates[1] - self.screen.get_height() + cos(radians(60)) * self.minimap.isometry.get_tile_length() * (UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height()))*coef_mul #*cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
                #     new_y -= self.screen.get_height() /2
                #     new_y -= 2*cos(radians(60)) * self.map.isometry.get_tile_length()
                #     print(new_x)
                #     Camera.set_camera(new_x, new_y)
        if pygame.mouse.get_pressed()[0]:
            coordinates = list(pygame.mouse.get_pos())
            # coordinates = list(event.pos)
            # coordinates[0] += self.screen.get_rect().x
            x, y = coordinates
            if (
                x >= self.screen.get_width() - self.minimap.minimap_width
                and y >= self.screen.get_height() - self.minimap.minimap_height
            ):

                coef_mul = (
                    self.map.isometry.get_tile_length()
                    / self.minimap.isometry.get_tile_length()
                )
                new_x = (
                    coordinates[0]
                    - self.screen.get_width()
                    + cos(radians(30))
                    * self.minimap.isometry.get_tile_length()
                    * UIManager.get_game().get_map().get_width()
                ) * coef_mul
                new_x -= self.screen.get_width() / 2

                new_y = (
                    coordinates[1]
                    - self.screen.get_height()
                    + cos(radians(60))
                    * self.minimap.isometry.get_tile_length()
                    * (
                        UIManager.get_game().get_map().get_width()
                        + UIManager.get_game().get_map().get_height()
                    )
                ) * coef_mul  # *cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
                new_y -= self.screen.get_height() / 2
                new_y -= 2 * cos(radians(60)) * self.map.isometry.get_tile_length()
                Camera.set_camera(new_x, new_y)
        self.screen.fill((61, 10, 7))

        offset = 5
        # if pygame.key.get_pressed()[pygame.K_r]:
        #     game = UIManager.get_game().get_map()
        #     buildings = list(game.get_buildings())[0]
        #     UIManager.get_game().get_map().remove_building(buildings)

        if self.correct_position:
            if (
                pygame.key.get_pressed()[pygame.K_LEFT]
                or pygame.key.get_pressed()[pygame.K_q]
            ):
                Camera.add_x(-offset)
            if (
                pygame.key.get_pressed()[pygame.K_RIGHT]
                or pygame.key.get_pressed()[pygame.K_d]
            ):
                Camera.add_x(offset)
            if (
                pygame.key.get_pressed()[pygame.K_UP]
                or pygame.key.get_pressed()[pygame.K_z]
            ):
                Camera.add_y(-offset)
            if (
                pygame.key.get_pressed()[pygame.K_DOWN]
                or pygame.key.get_pressed()[pygame.K_s]
            ):
                Camera.add_y(offset)

            offset = 40
            if (
                pygame.key.get_pressed()[pygame.K_LEFT]
                or pygame.key.get_pressed()[pygame.K_q]
            ) and (
                pygame.key.get_pressed()[pygame.K_LSHIFT]
                or pygame.key.get_pressed()[pygame.K_RSHIFT]
            ):
                Camera.add_x(-offset)
            if (
                pygame.key.get_pressed()[pygame.K_RIGHT]
                or pygame.key.get_pressed()[pygame.K_d]
            ) and (
                pygame.key.get_pressed()[pygame.K_LSHIFT]
                or pygame.key.get_pressed()[pygame.K_RSHIFT]
            ):
                Camera.add_x(offset)
            if (
                pygame.key.get_pressed()[pygame.K_UP]
                or pygame.key.get_pressed()[pygame.K_z]
            ) and (
                pygame.key.get_pressed()[pygame.K_LSHIFT]
                or pygame.key.get_pressed()[pygame.K_RSHIFT]
            ):
                Camera.add_y(-offset)
            if (
                pygame.key.get_pressed()[pygame.K_DOWN]
                or pygame.key.get_pressed()[pygame.K_s]
            ) and (
                pygame.key.get_pressed()[pygame.K_LSHIFT]
                or pygame.key.get_pressed()[pygame.K_RSHIFT]
            ):
                Camera.add_y(offset)

            if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
                Camera.zoom_in()
            if pygame.key.get_pressed()[pygame.K_KP_MINUS]:
                Camera.zoom_out()
        else:
            Camera.add_x(1)
            Camera.add_y(1)

        # clear the screen

        for resource in (
            UIManager.get_game().get_map().get_resources()
            - self.map.resource_points_objects
        ):
            self.map.add_resource_point(resource)
            self.minimap.add_resource_point(resource)
        for building in (
            UIManager.get_game().get_map().get_buildings() - self.map.buildings_objects
        ):
            self.map.add_building(building)
            self.minimap.add_building(building)
        for unit in UIManager.get_game().get_map().get_units() - self.map.units_objects:
            self.map.add_units(unit)
            self.minimap.add_units(unit)

        for resource in (
            self.map.resource_points_objects
            - UIManager.get_game().get_map().get_resources()
        ):
            self.map.remove_resource_point(resource)
            self.minimap.remove_resource_point(resource)
        for building in (
            self.map.buildings_objects - UIManager.get_game().get_map().get_buildings()
        ):
            self.map.remove_building(building)
            self.minimap.remove_building(building)
        for unit in self.map.units_objects - UIManager.get_game().get_map().get_units():
            self.map.remove_unit(unit)
            self.minimap.remove_unit(unit)

        # START CHRONO
        t = pygame.time.get_ticks()
        self.map.update()
        # print("Update time : ", pygame.time.get_ticks() - t)
        t = pygame.time.get_ticks()
        self.map.draw()
        # print("Draw time : ", pygame.time.get_ticks() - t)

        self.minimap.update()
        self.minimap.draw()

        coef = (
            self.map.isometry.get_tile_length()
            / self.minimap.isometry.get_tile_length()
        )

        rect = pygame.rect.Rect(
            0, 0, self.screen.get_width() / coef, self.screen.get_height() / coef
        )

        new_x = (
            Camera.get_x() + self.screen.get_width() / 2
        )  # - cos(radians(30)) * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
        new_x /= coef
        new_x -= (
            -self.screen.get_width()
            + cos(radians(30))
            * self.minimap.isometry.get_tile_length()
            * UIManager.get_game().get_map().get_width()
        )

        new_y = Camera.get_y()
        new_y += 2 * cos(radians(60)) * self.map.isometry.get_tile_length()
        new_y += self.screen.get_height() / 2
        new_y /= coef
        new_y -= -self.screen.get_height() + cos(
            radians(60)
        ) * self.minimap.isometry.get_tile_length() * (
            UIManager.get_game().get_map().get_width()
            + UIManager.get_game().get_map().get_height()
        )

        # new_y = (coordinates[1] - self.screen.get_height() + cos(
        #     radians(60)) * self.minimap.isometry.get_tile_length() * (
        #                  UIManager.get_game().get_map().get_width() + UIManager.get_game().get_map().get_height())) * coef_mul  # *cos(radians(30)) * coef_mul * self.minimap.isometry.get_tile_length() * UIManager.get_game().get_map().get_width()
        # new_y -= self.screen.get_height() / 2
        # new_y -= 2 * cos(radians(60)) * self.map.isometry.get_tile_length()

        rect.center = new_x, new_y
        # pygame.draw.rect(self.screen, (255, 0, 0), (new_x, new_y, self.screen.get_width()/coef, self.screen.get_height()/coef), 2)
        pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
        self.position_rect = rect
        x, y = rect.center
        self.correct_position = (
            x >= self.screen.get_width() - self.minimap.minimap_width
            and y >= self.screen.get_height() - self.minimap.minimap_height
        )
        if self.resources_showed:
            police = pygame.font.Font(None, 36)  # Police par défaut, taille 36
            texte = "Ressources joueurs :"
            texte_rendu = police.render(texte, True, (255, 255, 255))

            # Position du texte (en haut à droite)
            texte_rect = texte_rendu.get_rect()
            texte_rect.topright = (
                self.screen.get_width() - 10,
                10,
            )  # Décalage de 10 pixels du bord

            self.screen.blit(texte_rendu, texte_rect)
            x = 0
            for player in UIManager.get_game().get_players():
                police = pygame.font.Font(None, 36)  # Police par défaut, taille 36

                texte = (
                    "Joueur "
                    + str(player.get_color())
                    + " - Bois : "
                    + str(player.stock.get_wood())
                    + " - Nourriture : "
                    + str(player.stock.get_food())
                    + " - Or : "
                    + str(player.stock.get_gold())
                )
                texte_rendu = police.render(texte, True, (255, 255, 255))

                # Position du texte (en haut à droite)
                texte_rect = texte_rendu.get_rect()
                texte_rect.topright = (
                    self.screen.get_width() - 10,
                    x + 50,
                )  # Décalage de 10 pixels du bord
                x += 50
                self.screen.blit(texte_rendu, texte_rect)

        if UIManager.get_game().is_paused():
            texte = "Jeu en pause"
            police = pygame.font.Font(None, 36)  # Police par défaut, taille 36

            texte_rendu = police.render(texte, True, (255, 255, 255))

            # Position du texte (en haut à gauche)
            texte_rect = texte_rendu.get_rect()
            texte_rect.topleft = (10, 10)

            self.screen.blit(texte_rendu, texte_rect)

        # Display fps on the bottom left
        fps = self.clock.get_fps()
        police = pygame.font.Font(None, 18)
        texte = "FPS : " + str(int(fps))
        texte_rendu = police.render(texte, True, (255, 255, 255))
        texte_rect = texte_rendu.get_rect()
        texte_rect.bottomleft = (10, self.screen.get_height() - 10)
        self.screen.blit(texte_rendu, texte_rect)

        # print("Camera", Camera.get_x(), Camera.get_y())

        pygame.display.flip()

        # tick the clock
        self.clock.tick(1000)
        import time
        time.sleep(0.1)
        UIManager.get_game().party()

    def cleanup(self):
        pass
