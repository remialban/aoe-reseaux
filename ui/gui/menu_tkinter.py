import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MenuTkinter:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Menu")
        self.master.geometry("800x600")  # Taille de la fenêtre principale

        # Chargement et redimensionnement de l'image de fond
        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Affichage de l'image de fond
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Style des boutons
        button_style = {
            "bg": "white",
            "font": ("Helvetica", 14),
            "fg": "black",
            "relief": "solid",
            "borderwidth": 2
        }

        # Boutons
        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game, **button_style)
        self.new_game_button.place(x=350, y=150)

        self.load_game_button = tk.Button(self.master, text="Load Game", command=self.load_game, **button_style)
        self.load_game_button.place(x=350, y=200)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game, **button_style)
        self.quit_button.place(x=350, y=250)
        
        # Bouton Join Online Game
        self.join_online_game_button = tk.Button(self.master, text="Join Online Game", command=self.join_online_game, **button_style)
        self.join_online_game_button.place(x=350, y=300)  # Place au bon endroit

        print("Join Online Game button created.")

    def new_game(self):
        self.clear_menu()
        NewGameMenu(self.master, self.bg_photo)

    def load_game(self):
        print("Load game selected.")
        messagebox.showinfo("Load Game", "Game loaded!")

    def quit_game(self):
        print("Quit game selected.")
        self.master.quit()

    def clear_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
            
    def join_online_game(self):
        print("Join Online Game clicked.")

class NewGameMenu:
    def __init__(self, master, bg_photo):
        self.master = master
        self.bg_photo = bg_photo

        # Chargement et redimensionnement du fond d'écran
        self.bg_image = Image.open("assets/background.jpg")
        self.bg_image = self.bg_image.resize((900, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Style des boutons
        button_style = {
            "bg": "white",
            "font": ("Helvetica", 14),
            "fg": "black",
            "relief": "solid",
            "borderwidth": 2,
        }

        label_style = {
            "bg": "white",
            "font": ("Helvetica", 14, "bold"),
            "fg": "black",
        }

        center_x = 400

        # Label "Number of Players"
        self.players_label = tk.Label(self.master, text="Number of Players:", **label_style)
        self.players_label.place(x=center_x, y=50)

        # Menu déroulant pour choisir le nombre de joueurs (1 à 8)
        self.players_var = tk.IntVar(value=1)
        self.players_dropdown = tk.OptionMenu(self.master, self.players_var, *range(1, 9))
        self.players_dropdown.config(**button_style)
        self.players_dropdown.place(x=center_x + 180, y=50)

        # Label "Map Size"
        self.map_size_label = tk.Label(self.master, text="Map Size:", **label_style)
        self.map_size_label.place(x=center_x, y=140)

        # Sliders pour la taille de la carte
        self.map_width_slider = tk.Scale(
            self.master, from_=50, to=400, resolution=10, orient=tk.HORIZONTAL,
            label="Width", length=300, **button_style
        )
        self.map_width_slider.place(x=center_x, y=180)

        self.map_height_slider = tk.Scale(
            self.master, from_=50, to=400, resolution=10, orient=tk.HORIZONTAL,
            label="Height", length=300, **button_style
        )
        self.map_height_slider.place(x=center_x, y=250)

        # Labels et menus déroulants pour le mode de ressources et les conditions de départ
        self.resource_variation_button = tk.Label(self.master, text="Map Mode", **label_style)
        self.resource_variation_button.place(x=center_x, y=350)

        self.starting_conditions_button = tk.Label(self.master, text="Starting Conditions", **label_style)
        self.starting_conditions_button.place(x=center_x + 200, y=350)

        self.resource_mode_option_var = tk.StringVar(value="Gold Rush")
        self.resource_mode_option_menu = tk.OptionMenu(
            self.master, self.resource_mode_option_var, "Gold Rush", "Generous", "Normal"
        )
        self.resource_mode_option_menu.config(**button_style)
        self.resource_mode_option_menu.place(x=center_x, y=400)

        self.starting_resources_option_var = tk.StringVar(value="Lean")
        self.starting_resources_option_menu = tk.OptionMenu(
            self.master, self.starting_resources_option_var, "Lean", "Mean", "Marines"
        )
        self.starting_resources_option_menu.config(**button_style)
        self.starting_resources_option_menu.place(x=center_x + 200, y=400)

        # Boutons "Start Game" et "Back"
        self.start_button = tk.Button(
            self.master, text="Start Game", command=self.start_game, **button_style
        )
        self.start_button.place(x=center_x + 200, y=500)

        self.back_button = tk.Button(
            self.master, text="Back", command=self.back_to_main_menu, **button_style
        )
        self.back_button.place(x=center_x, y=500)

    def start_game(self):
        players = self.players_var.get()
        map_width = self.map_width_slider.get()
        map_height = self.map_height_slider.get()
        resource_mode = self.resource_mode_option_var.get()
        starting_resources = self.starting_resources_option_var.get()

        print(
            f"Starting game with {players} player(s), map size {map_width}x{map_height}, resource mode {resource_mode}, starting resources {starting_resources}."
        )

    def back_to_main_menu(self):
        self.cleanup()
        MenuTkinter(self.master)

    def cleanup(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    

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

        # Style pour le titre
        title_style = {
            "font": ("Helvetica", 22, "bold"),
            "bg": "#D9D9D9",
            "fg": "black",
            "padx": 10,
            "pady": 5,
            "relief": "solid",
            "borderwidth": 3
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

        # Titre du menu
        self.title_label = tk.Label(self.master, text="Join Online Game", **title_style)
        self.title_label.place(x=center_x - 100, y=40)

        # Nom du serveur
        self.server_name_label = tk.Label(self.master, text="Server Name:", **label_style)
        self.server_name_label.place(x=center_x - 100, y=100)
        self.server_name_entry = tk.Entry(self.master, **entry_style)
        self.server_name_entry.place(x=center_x - 100, y=130)

        # Nombre de joueurs
        self.players_count_label = tk.Label(self.master, text="Players in Game:", **label_style)
        self.players_count_label.place(x=center_x - 100, y=170)
        self.players_count_value = tk.Label(self.master, text="0", **label_style)
        self.players_count_value.place(x=center_x + 80, y=170)

        # Bouton pour rejoindre la partie
        self.join_button = tk.Button(self.master, text="Join Game", command=self.join_game, **button_style)
        self.join_button.place(x=center_x - 90, y=220)

        # Bouton pour revenir au menu principal
        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main_menu, **button_style)
        self.back_button.place(x=center_x - 90, y=270)

    def add_hover_effect(self, button):
        """Ajoute un effet de survol pour changer la couleur du bouton."""
        button.bind("<Enter>", lambda e: button.config(bg="#BFBFBF"))  # Gris plus foncé au survol
        button.bind("<Leave>", lambda e: button.config(bg="#D9D9D9"))  # Revenir à la couleur initiale

    def join_game(self):
        server_name = self.server_name_entry.get()
        print(f"Attempting to join server: {server_name}")
        # Ajouter ici la logique pour rejoindre le serveur.

    def back_to_main_menu(self):
        self.cleanup()
        MenuTkinter(self.master)  # Retour au menu principal

    def cleanup(self):
        # Supprimer tous les widgets du menu actuel
        for widget in self.master.winfo_children():
            widget.destroy()
