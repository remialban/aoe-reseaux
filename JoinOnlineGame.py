
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
