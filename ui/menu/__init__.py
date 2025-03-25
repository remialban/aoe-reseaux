import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from core import Game, Player, Map
from core.buildings.barracks import Barracks
from core.buildings.house import House
from core.buildings.stable import Stable
from core.players import Player
from core.players.ai import AI
from core.players import Resource
from core.buildings import Building
from core.buildings.town_center import TownCenter
from core.position import Position
from core.resource import Resource
from core.resources_points.mine import Mine
from core.resources_points.wood import Wood
from core.resources_points import ResourcePoint
from core.units import Unit
from random import randint
from core.units.villager import Villager
from core.map import RessourceModes, PlayerModes
from network.sender import Sender
from network.state import State
from ui import UI
from ui.enums import UIList
from ui.ui_manager import UIManager
from core.map import Map
from network.receiver import Receiver, get_available_colors


class MENU(UI):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.root = tk.Tk()

    def update(self):
        pass

    def cleanup(self):
        self.root.quit()
        self.root.destroy()

    def loop(self):
        menu = MenuTkinter(self.root)
        self.root.mainloop()


class MenuTkinter:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Menu")
        self.master.geometry("800x600")

        self.bg_image = Image.open("assets/background.jpg")
        self.bg_image = self.bg_image.resize((900, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {
            "bg": "white",
            "font": ("Helvetica", 14),
            "fg": "black",
            "relief": "solid",
            "borderwidth": 2,
        }

        self.new_game_button = tk.Button(
            self.master, text="Create Online Game", command=self.new_game, **button_style
        )
        self.new_game_button.pack(pady=10)

        self.load_game_button = tk.Menubutton(
            self.master, text="Load Game", **button_style, direction="below"
        )
        self.load_game_button.pack(pady=10)
        self.load_game_menu = tk.Menu(self.load_game_button, tearoff=0)
        self.load_game_button.configure(menu=self.load_game_menu)

        self.populate_load_game_menu()
        
          # Bouton Join Online Game
        self.join_online_game_button = tk.Button(self.master, text="Join Online Game", command=self.join_online_game, **button_style)
        self.join_online_game_button.pack(pady=10)  # Place au bon endroit

        print("Join Online Game button created.")

        self.quit_button = tk.Button(
            self.master, text="Quit", command=self.quit_game, **button_style
        )
        self.quit_button.pack(pady=10)

        self.master.bind("<KeyPress>", self.on_key_press)

    def on_key_press(self, event):
        if event.keysym == "F9":
            UIManager.get_current_ui().cleanup()
            UIManager.change_ui(UIList.CLI)
            UIManager.get_current_ui().cleanup()

    def populate_load_game_menu(self):
        self.load_game_menu.delete(0, tk.END)

        backups = UIManager.get_backups()
        if backups:
            for backup in backups:
                self.load_game_menu.add_command(
                    label=backup, command=lambda b=backup: self.load_game(b)
                )
        else:
            self.load_game_menu.add_command(
                label="No backups available", state=tk.DISABLED
            )

    def new_game(self):
        self.clear_menu()
        NewGameMenu(self.master, self.bg_photo)
        
    def join_online_game(self):
        self.clear_menu()
        JoinOnlineGameMenu(self.master, self.bg_photo)

    def load_game(self, backup_name):
        print(f"Loading game: {backup_name}")
        UIManager.load_game(backup_name)
        UIManager.get_current_ui().cleanup()
        UIManager.change_ui(UIList.GUI)

    def quit_game(self):
        print("Quit game selected.")
        self.master.quit()
        UIManager.stop()

    def clear_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()


RESOURCE_MODE_MAP = {
    "Gold Rush": RessourceModes.GOLD_RUSH,
    "Generous": RessourceModes.GENEROUS,
    "Normal": RessourceModes.NORMAL,
}


class NewGameMenu:
    def __init__(self, master, bg_photo):
        self.master = master
        self.bg_photo = bg_photo
        self.bg_image = Image.open("assets/background.jpg")
        self.bg_image = self.bg_image.resize((900, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {
            "bg": "white",
            "font": ("Helvetica", 14),
            "fg": "black",
            "relief": "solid",
            "borderwidth": 2,
        }

        center_x = 400
        self.players_label = tk.Label(
            self.master, text="Number of Players:", **button_style
        )
        self.players_label.place(x=center_x, y=50)
        self.players_var = tk.IntVar(value=1)
        self.players_option0 = tk.Radiobutton(
            self.master,
            text="0 Player",
            variable=self.players_var,
            value=0,
            **button_style,
        )
        self.players_option1 = tk.Radiobutton(
            self.master,
            text="1 Player",
            variable=self.players_var,
            value=1,
            **button_style,
        )
        self.players_option2 = tk.Radiobutton(
            self.master,
            text="2 Players",
            variable=self.players_var,
            value=2,
            **button_style,
        )
        self.players_option0.place(x=center_x - 100, y=90)
        self.players_option1.place(x=center_x, y=90)
        self.players_option2.place(x=center_x + 100, y=90)

        self.map_size_label = tk.Label(self.master, text="Map Size:", **button_style)
        self.map_size_label.place(x=center_x, y=140)
        self.map_width_slider = tk.Scale(
            self.master,
            from_=50,
            to=400,
            resolution=10,
            orient=tk.HORIZONTAL,
            label="Width",
            length=300,
            **button_style,
        )
        self.map_width_slider.place(x=center_x, y=180)
        self.map_height_slider = tk.Scale(
            self.master,
            from_=50,
            to=400,
            resolution=10,
            orient=tk.HORIZONTAL,
            label="Height",
            length=300,
            **button_style,
        )
        self.map_height_slider.place(x=center_x, y=250)

        self.resource_variation_button = tk.Label(
            self.master, text="Map Mode", **button_style
        )
        self.resource_variation_button.place(x=center_x, y=350)

        self.starting_conditions_button = tk.Label(
            self.master, text="Starting Conditions", **button_style
        )
        self.starting_conditions_button.place(x=center_x + 200, y=350)

        self.resource_mode_option_var = tk.StringVar(value="Gold Rush")
        self.resource_mode_option_menu = tk.OptionMenu(
            self.master,
            self.resource_mode_option_var,
            "Gold Rush",
            "Generous",
            "Normal",
        )
        self.resource_mode_option_menu.config(**button_style)
        self.resource_mode_option_menu.place(x=center_x, y=400)

        self.starting_resources_option_var = tk.StringVar(value="Lean")
        self.starting_resources_option_menu = tk.OptionMenu(
            self.master, self.starting_resources_option_var, "Lean", "Mean", "Marines"
        )
        self.starting_resources_option_menu.config(**button_style)
        self.starting_resources_option_menu.place(x=center_x + 200, y=400)

        self.start_button = tk.Button(
            self.master, text="Start Game", command=self.start_game, **button_style
        )
        self.start_button.place(x=center_x + 200, y=500)

        self.back_button = tk.Button(
            self.master, text="Back", command=self.back_to_main_menu, **button_style
        )
        self.back_button.place(x=center_x, y=500)

    def start_game(self):
        State.set_receiving(True)
        players = self.players_var.get()
        map_width = self.map_width_slider.get()
        map_height = self.map_height_slider.get()
        resource_mode = self.resource_mode_option_var.get()
        starting_resources = self.starting_resources_option_var.get()

        print(
            f"Starting game with {players} player(s), map size {map_width}x{map_height}, resource mode {resource_mode}, starting resources {starting_resources}."
        )

        # player1 = Player("eee", "MAGENTA")
        # player2 = Player("eee", "RED")
        player1 = AI("Selma", "RED")
        player2 = AI("Remi ;)", "YELLOW", strategy="defensive")

        if players == 0:
            players_set = set()
        elif players == 1:
            players_set = {player1}
        else:
            players_set = {player1, player2}

        if starting_resources == "Lean":
            player1.stock = Resource(0, 0, 0)
            player1.town_centers = [
                Building(
                    10, 5, 1000, Position(0, 0), 10, True, Resource(0, 0, 0), player1
                )
            ]
            player1.villagers = [
                Villager("Villager 1", player1),
                Villager("Villager 2", player1),
                Villager("Villager 3", player1),
            ]
        elif starting_resources == "Mean":
            player1.stock = Resource(2000, 2000, 2000)
            player1.town_centers = [
                Building(
                    10,
                    5,
                    1000,
                    Position(0, 0),
                    10,
                    True,
                    Resource(200, 100, 100),
                    player1,
                )
            ]
            player1.villagers = [
                Villager("Villager 1", player1),
                Villager("Villager 2", player1),
                Villager("Villager 3", player1),
            ]
        elif starting_resources == "Marines":
            player1.stock = Resource(20000, 20000, 20000)
            player1.town_centers = [
                Building(
                    10,
                    5,
                    1000,
                    Position(0, 0),
                    10,
                    True,
                    Resource(200, 100, 100),
                    player1,
                ),
                Building(
                    10,
                    5,
                    1000,
                    Position(10, 0),
                    10,
                    True,
                    Resource(200, 100, 100),
                    player1,
                ),
                Building(
                    10,
                    5,
                    1000,
                    Position(20, 0),
                    10,
                    True,
                    Resource(200, 100, 100),
                    player1,
                ),
            ]
            player1.villagers = [
                Villager("Villager 1", player1),
                Villager("Villager 2", player1),
                Villager("Villager 3", player1),
                Villager("Villager 4", player1),
                Villager("Villager 5", player1),
                Villager("Villager 6", player1),
                Villager("Villager 7", player1),
                Villager("Villager 8", player1),
                Villager("Villager 9", player1),
                Villager("Villager 10", player1),
                Villager("Villager 11", player1),
                Villager("Villager 12", player1),
                Villager("Villager 13", player1),
                Villager("Villager 14", player1),
                Villager("Villager 15", player1),
            ]
            player1.barracks = [
                Building(
                    10,
                    5,
                    800,
                    Position(30, 0),
                    10,
                    True,
                    Resource(300, 150, 100),
                    player1,
                )
                for _ in range(2)
            ]
            player1.stables = [
                Building(
                    10,
                    5,
                    800,
                    Position(40, 0),
                    10,
                    True,
                    Resource(300, 150, 100),
                    player1,
                )
                for _ in range(2)
            ]
            player1.archery_ranges = [
                Building(
                    10,
                    5,
                    800,
                    Position(50, 0),
                    10,
                    True,
                    Resource(300, 150, 100),
                    player1,
                )
                for _ in range(2)
            ]

        State.set_receiving(False)
        for p in players_set:
            Sender.notify_add(p)
        State.set_receiving(True)
        map = Map(
            map_width,
            map_height,
            RESOURCE_MODE_MAP[resource_mode],
            PlayerModes[starting_resources.upper()],
            players_set,
        )
        State.set_receiving(True)

        for b in map.buildings:
            Sender.notify_add(b)
        for r in map.resources_points:
            Sender.notify_add(r)

        for u in map.units:
            Sender.notify_add(u)




        game = Game(players=players_set, map=map)
        State.set_receiving(False)

        UIManager.set_game(game)
        UIManager.get_current_ui().cleanup()
        UIManager.change_ui(UIList.GUI)

    def back_to_main_menu(self):
        self.cleanup()
        MenuTkinter(self.master)

    def cleanup(self):
        for widget in self.master.winfo_children():
            widget.destroy()


# Définir les couleurs
COLORS = {
    "RED": 1,
    "GREEN": 2,
    "YELLOW": 3,
    "BLUE": 4,
    "MAGENTA": 5,
    "CYAN": 6,
    "WHITE": 7
}

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from core import Game, Player, Map, Action  # Assure-toi que ces classes existent et sont importées

# Définir les couleurs
COLORS = {
    "RED": 1,
    "GREEN": 2,
    "YELLOW": 3,
    "BLUE": 4,
    "MAGENTA": 5,
    "CYAN": 6,
    "WHITE": 7
}

class JoinOnlineGameMenu:
    def __init__(self, master, bg_photo):
        self.master = master
        self.bg_photo = bg_photo

        # Redimensionner et configurer l'image de fond
        self.bg_image = Image.open("assets/background.jpg")
        self.bg_image = self.bg_image.resize((900, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Style des boutons
        button_style = {
            "bg": "#D9D9D9",  # Gris clair
            "fg": "black",
            "font": ("Helvetica", 14, "bold"),
            "relief": "ridge",
            "borderwidth": 3,
            "width": 20,
            "height": 1,
            "cursor": "hand2"
        }

        # Style pour les labels
        label_style = {
            "font": ("Helvetica", 14, "bold"),
            "bg": "#D9D9D9",
            "fg": "black",
            "padx": 5,
            "pady": 2
        }

        # Style pour les champs de saisie
        entry_style = {
            "font": ("Helvetica", 14),
            "width": 22,
            "relief": "solid",
            "borderwidth": 2
        }

        # Centrage horizontal
        center_x = 450

        # Nom du joueur
        self.server_name_label = tk.Label(self.master, text="Player Name:", **label_style)
        self.server_name_label.place(x=center_x - 90, y=100)
        self.server_name_entry = tk.Entry(self.master, **entry_style)
        self.server_name_entry.place(x=center_x - 90, y=130)

        # Menu déroulant pour choisir la couleur
        self.color_label = tk.Label(self.master, text="Choose Color:", **label_style)
        self.color_label.place(x=center_x - 90, y=170)

        # Variable pour stocker la couleur choisie
        self.color_var = tk.StringVar()
        self.color_var.set(list(COLORS.keys())[0])  # Valeur par défaut (RED)

        # Menu déroulant
        self.color_menu = tk.OptionMenu(self.master, self.color_var, *COLORS.keys())
        self.color_menu.config(font=("Helvetica", 14), width=15)
        self.color_menu.place(x=center_x + 90, y=170)

        # Bouton pour rejoindre la partie
        self.join_button = tk.Button(self.master, text="Join Game", command=self.join_game, **button_style)
        self.join_button.place(x=center_x - 90, y=210)

        # Bouton pour revenir au menu principal
        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main_menu, **button_style)
        self.back_button.place(x=center_x - 90, y=260)
        
        available_colors = get_available_colors()
        
        # Update color selection menu
        self.color_label = tk.Label(self.master, text="Choose Color:", **label_style)
        self.color_label.place(x=center_x - 90, y=170)

        # Variable for storing chosen color
        self.color_var = tk.StringVar()
        if available_colors:  # Set default value only if colors are available
            self.color_var.set(available_colors[0])
            
            # Create color menu with available colors
            self.color_menu = tk.OptionMenu(self.master, self.color_var, *available_colors)
            self.color_menu.config(font=("Helvetica", 14), width=15)
            self.color_menu.place(x=center_x + 90, y=170)
            
            # Enable join button
            self.join_button = tk.Button(
                self.master, 
                text="Join Game", 
                command=self.join_game,
                state="normal",
                **button_style
            )
        else:
            # Show message if no colors available
            tk.Label(
                self.master,
                text="No colors available - Game is full",
                font=("Helvetica", 12),
                fg="red",
                bg="#D9D9D9"
            ).place(x=center_x - 90, y=170)
            
            # Disable join button
            self.join_button = tk.Button(
                self.master, 
                text="Join Game", 
                command=self.join_game,
                state="disabled",
                **button_style
            )
        
        self.join_button.place(x=center_x - 90, y=210)    
        
        

    def join_game(self):
        """Crée une partie avec les paramètres prédéfinis et lance la partie."""
        from core import Game  # Import de la classe Game
        from core import Player  # Import de la classe Player
        from core import Map  # Import de la classe Map

        # Récupérer le nom du joueur et la couleur sélectionnée
        player_name = self.server_name_entry.get()
        chosen_color = self.color_var.get()

        # Vérifier que le joueur a bien entré un nom
        if not player_name:
            print("Error: Player name cannot be empty!")
            return

        # Créer un joueur avec la couleur choisie
        player = Player(name=player_name, color=chosen_color)

        # Générer une carte 50x50 en mode Gold Rush
        game_map = Map(width = 50,height= 50,ressource_mode=RessourceModes.GOLD_RUSH, player_mode =PlayerModes.LEAN, players= {player})

        # Initialiser la partie avec un seul joueur
        game = Game(players={player}, map=game_map)

        # Démarrer la boucle de jeu
        State.set_receiving(False)

        UIManager.set_game(game)
        UIManager.get_current_ui().cleanup()
        UIManager.change_ui(UIList.GUI)


    def back_to_main_menu(self):
        self.cleanup()
        MenuTkinter(self.master)  # Retour au menu principal

    def cleanup(self):
        """Supprime tous les widgets du menu actuel."""
        for widget in self.master.winfo_children():
            widget.destroy()