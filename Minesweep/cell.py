# MultipleFiles/cell.py
from tkinter import *
from tkinter import Button, Label, Tk  
import random
import setup
import sys
import webbrowser
from utils import center_window
import pygame
import time

def bgm(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def stop_bgm():
    pygame.mixer.music.stop()

class Cell:
    all = []
    start_time = 0
    cell_count = setup.CELL_COUNT
    cell_count_label_object = None
    flag_count = 0
    flag_count_label_object = None
    is_game_over = False

    def __init__(self, x, y, is_bom=False):
        self.is_bom = is_bom
        self.is_opened = False
        self.is_bom_chance = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # append object ke Cell.all list
        Cell.all.append(self)


    def on_enter(self, event):
        if not self.is_opened and not self.is_bom_chance:
            self.cell_btn_object.configure(bg='lightgray')

    def on_leave(self, event):
        if not self.is_opened and not self.is_bom_chance:
            self.cell_btn_object.configure(bg='SystemButtonFace')


    def create_btn_object(self, loct):
        btn = Button(
            loct,
            width=12, 
            height=4,
        )
        btn.bind("<Enter>", self.on_enter, lambda e: btn.configure(bg="#d1d8e0"))  # Hover in
        btn.bind("<Leave>", self.on_leave, lambda e: btn.configure(bg="SystemButtonFace"))  # Hover out
        btn.bind('<Button-1>', self.L_click)  # lmb event
        btn.bind('<Button-3>', self.R_click)  # rmb event
        self.cell_btn_object = btn

    @staticmethod
    def count_label(loct):
        lbl = Label(
            loct,
            bg='#34495e',
            fg='white',
            text=f"Cell Tersisa:{Cell.cell_count}",
            width=18,
            height=4,
            font=("", 30),
            justify=LEFT
        )
        Cell.cell_count_label_object = lbl

    def L_click(self, event):
        if self.is_bom:
            self.show_bom()
            self.game_over()  # Panggil fungsi game_over saat menyentuh bom
        else:
            if self.cell_area_bom_length == 0:
                for cell_obj in self.cell_area:
                    cell_obj.show_cell()
            self.show_cell()
            # win condition mines == cell sisa
            if Cell.cell_count == setup.BOM:
                self.win_game()  # Panggil fungsi game_over saat menang

        # cancel l & r click event klo cell dh kebuka 
        if self.cell_btn_object.winfo_exists():
            self.cell_btn_object.unbind('<Button-1>')
            self.cell_btn_object.unbind('<Button-3>')
    def cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
            
    def R_click(self, event):
        if not self.is_bom_chance:
            self.cell_btn_object.configure(bg='orange')
            self.is_bom_chance = True
            Cell.flag_count += 1
        else:
            self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_bom_chance = False
            Cell.flag_count -= 1

        # label bendera
        if Cell.flag_count_label_object:
            Cell.flag_count_label_object.configure(
                text=f"🚩 Bendera: {Cell.flag_count}"
            )


    @property        
    def cell_area(self):
        cells = [
            self.cell_by_axis(self.x - 1, self.y - 1),
            self.cell_by_axis(self.x - 1, self.y),
            self.cell_by_axis(self.x - 1, self.y + 1),
            self.cell_by_axis(self.x, self.y - 1),
            self.cell_by_axis(self.x + 1, self.y - 1),
            self.cell_by_axis(self.x + 1, self.y),
            self.cell_by_axis(self.x + 1, self.y + 1),
            self.cell_by_axis(self.x, self.y + 1),
        ]
        
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def cell_area_bom_length(self):
        counter = 0
        for cell in self.cell_area:
            if cell.is_bom:
                counter += 1

        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.cell_area_bom_length)
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cell Tersisa:{Cell.cell_count}"
                )
            # ganti warna cell ke default just in case warnanya keganti
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
        self.is_opened = True

        if self.cell_area_bom_length == 0:  
            for cell in self.cell_area:
                if not cell.is_opened:
                    cell.show_cell()

    def show_bom(self):
        self.cell_btn_object.configure(bg='red')
        self.game_over()  # Panggil fungsi game_over saat menyentuh bom

    @staticmethod
    def flag_label(loct):
        lbl = Label(
            loct,
            bg='#34495e',
            fg='white',
            text=f"🚩 Bendera: {Cell.flag_count}",
            width=21,
            height=3,
            justify=LEFT,
            font=("Arial", 24)
        )
        Cell.flag_count_label_object = lbl


    @staticmethod
    def randomize_boms():
        picked_cells = random.sample(
            Cell.all, setup.BOM
        )
        for picked_cell in picked_cells:
            picked_cell.is_bom = True

    @staticmethod
    def game_over():
        stop_bgm()
        if Cell.is_game_over:
            return
        
        Cell.is_game_over = True

        try:
        # Tutup jendela utama jika ada
            if hasattr(Cell, 'main_window') and Cell.main_window is not None:
                Cell.main_window.destroy()  # Tutup jendela utama
        except: 
            pass

        # Jendela Game Over
        game_over_window = Tk()
        game_over_window.title("Game Over")
        center_window(game_over_window, 400, 300) 
        game_over_window.configure(bg='lightcoral')

        # Label Game Over
        Label(game_over_window, text="Game Over!", font=("Arial", 24), bg='lightcoral', fg='white').pack(pady=20)

        # Tombol untuk kembali ke title screen
        Button(game_over_window, text="Kembali ke Title Screen", command=lambda: Cell.restart_game(game_over_window), font=("Arial", 14), bg='lightgreen').pack(pady=10)
        # Tombol untuk keluar
        Button(game_over_window, text="Keluar", command=sys.exit, font=("Arial", 14), bg='red').pack(pady=10)

        game_over_window.mainloop()

    @staticmethod
    def win_game():
        stop_bgm()
        if Cell.is_game_over:
            return

        Cell.is_game_over = True

        try:
            if hasattr(Cell, 'main_window') and Cell.main_window is not None:
                Cell.main_window.destroy()
        except:
            pass

        webbrowser.open("https://www.youtube.com/watch?v=oyFQVZ2h0V8")

        elapsed = int(time.time() - Cell.start_time)

        win_window = Tk()
        win_window.title("Selamat!")
        center_window(win_window, 400, 300)
        win_window.configure(bg='lightgreen')  # Hijau muda
        

        Label(win_window, text=f"Kamu Menang!\nWaktu: {elapsed} detik", font=("Arial", 24), bg='lightgreen', fg='white', justify='center').pack(pady=20)

        Button(win_window, text="Kembali ke Title Screen", command=lambda: Cell.restart_game(win_window), font=("Arial", 14), bg='white').pack(pady=10)
        Button(win_window, text="Keluar", command=sys.exit, font=("Arial", 14), bg='red').pack(pady=10)

        win_window.mainloop()

    @staticmethod
    def restart_game(game_over_window):
        game_over_window.destroy()  # Tutup jendela Game Over
        from mine import title_screen  # Import title_screen dari mine.py
        title_screen()  # Kembali ke title screen

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"