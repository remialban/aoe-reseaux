
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
        player1 = AI("Selma", "BLUE")
        player2 = AI("Remi ;)", "YELLOW", strategy="defensive")

        if players == 0:
            players_set = set()
        elif players == 1:
            players_set = {player1}
        else:
            players_set = {player1, player2}

        """
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
        """
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
