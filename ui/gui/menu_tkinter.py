import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MenuTkinter:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Menu")
        self.master.geometry("800x600")

        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {"bg": "white", "font": ("Helvetica", 14), "fg": "black", "relief": "solid", "borderwidth": 2}

        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game, **button_style)
        self.new_game_button.pack(pady=10)

        self.load_game_button = tk.Button(self.master, text="Load Game", command=self.load_game, **button_style)
        self.load_game_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game, **button_style)
        self.quit_button.pack(pady=10)

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

class NewGameMenu:
    def __init__(self, master, bg_photo):
        self.master = master

        self.bg_label = tk.Label(self.master, image=bg_photo)
        self.bg_label.image = bg_photo
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {"bg": "white", "font": ("Helvetica", 14), "fg": "black", "relief": "solid", "borderwidth": 2}

        self.title_label = tk.Label(self.master, text="New Game Settings", **button_style)
        self.title_label.pack(pady=10)

        # Number of Players
        self.players_label = tk.Label(self.master, text="Number of Players:", **button_style)
        self.players_label.pack(pady=5)
        self.players_var = tk.IntVar(value=1)
        self.players_option1 = tk.Radiobutton(self.master, text="1 Player", variable=self.players_var, value=1, **button_style)
        self.players_option2 = tk.Radiobutton(self.master, text="2 Players", variable=self.players_var, value=2, **button_style)
        self.players_option1.pack(pady=2)
        self.players_option2.pack(pady=2)

        # Map Size
        self.map_size_label = tk.Label(self.master, text="Map Size:", **button_style)
        self.map_size_label.pack(pady=5)
        self.map_size_var = tk.StringVar(value="120x120")
        self.map_size_option1 = tk.Radiobutton(self.master, text="120x120", variable=self.map_size_var, value="120x120", **button_style)
        self.map_size_option2 = tk.Radiobutton(self.master, text="168x168", variable=self.map_size_var, value="168x168", **button_style)
        self.map_size_option1.pack(pady=2)
        self.map_size_option2.pack(pady=2)

        # Map Mode
        self.map_mode_label = tk.Label(self.master, text="Map Mode:", **button_style)
        self.map_mode_label.pack(pady=5)
        self.map_mode_var = tk.StringVar(value="Resource Variation")
        self.map_mode_option1 = tk.Radiobutton(self.master, text="Resource Variation", variable=self.map_mode_var, value="Resource Variation", **button_style)
        self.map_mode_option2 = tk.Radiobutton(self.master, text="Starting Resources", variable=self.map_mode_var, value="Starting Resources", **button_style)
        self.map_mode_option1.pack(pady=2)
        self.map_mode_option2.pack(pady=2)

        # Start Button
        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, **button_style)
        self.start_button.pack(pady=10)

        # Back Button
        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main_menu, **button_style)
        self.back_button.pack(pady=10)

    def start_game(self):
        players = self.players_var.get()
        map_size = self.map_size_var.get()
        map_mode = self.map_mode_var.get()
        print(f"Starting game with {players} player(s), map size {map_size}, map mode {map_mode}.")
        messagebox.showinfo("Start Game", f"Game started with {players} player(s), map size {map_size}, map mode {map_mode}!")

    def back_to_main_menu(self):
        self.clear_menu()
        MenuTkinter(self.master)

    def clear_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

def show_menu():
    root = tk.Tk()
    menu = MenuTkinter(root)
    root.mainloop()

if __name__ == "__main__":
    show_menu()
