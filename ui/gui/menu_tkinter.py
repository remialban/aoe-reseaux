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


        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game, bg="lightblue", font=("Helvetica", 14))
        self.new_game_button.pack(pady=10)

        self.load_game_button = tk.Button(self.master, text="Load Game", command=self.load_game, bg="lightgreen", font=("Helvetica", 14))
        self.load_game_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game, bg="salmon", font=("Helvetica", 14))
        self.quit_button.pack(pady=10)

    def new_game(self):
        print("New game started.")
        messagebox.showinfo("New Game", "New game started!")
        self.master.quit()

    def load_game(self):
        print("Load game selected.")
        messagebox.showinfo("Load Game", "Game loaded!")
        self.master.quit()

    def quit_game(self):
        print("Quit game selected.")
        self.master.quit()



def show_menu():
    root = tk.Tk()
    menu = MenuTkinter(root)
    root.mainloop()


if __name__ == "__main__":
    show_menu()
