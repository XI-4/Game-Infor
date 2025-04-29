# MultipleFiles/mine.py
from tkinter import *
from tkinter import PhotoImage
from tkinter.ttk import Progressbar, Style
from cell import Cell
import setup
import utils
from utils import center_window
import pygame
import time

#inisialisasi pygame (music purpose)
pygame.mixer.init()

def bgm(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def stop_bgm():
    pygame.mixer.music.stop()
    
def title_screen():
    stop_bgm()
    title_window = Tk()
    title_window.title("Minesweeper")
    center_window(title_window, 800, 600)
    title_window.configure(bg='lightblue')

    bgm("bgm\soundtitle.mp3")

    # Judul Game
    title_label = Label(title_window, text="Minesweeper", font=("Arial", 48, "bold"), bg='lightblue', fg='darkblue')
    title_label.pack(pady=20)

    # Label untuk memilih tingkat kesulitan
    difficulty_label = Label(title_window, text="Pilih Tingkat Kesulitan:", font=("Arial", 24), bg='lightblue', fg='darkblue')
    difficulty_label.pack(pady=10)

    # Tombol untuk memilih tingkat kesulitan
    Button(title_window, text="Mudah", command=lambda: start_game('easy', title_window), font=("Arial", 18), bg='lightgreen').pack(pady=5)
    Button(title_window, text="Sedang", command=lambda: start_game('medium', title_window), font=("Arial", 18), bg='yellow').pack(pady=5)
    Button(title_window, text="Sulit", command=lambda: start_game('hard', title_window), font=("Arial", 18), bg='red').pack(pady=5)

    title_window.mainloop()

def start_game(difficulty, title_window):
    setup.update_settings(difficulty)  # Update pengaturan berdasarkan tingkat kesulitan
    title_window.destroy()  # Tutup title screen
    main_game()  # Panggil fungsi utama game

def main_game():
    global root
    stop_bgm()
    bgm("bgm\soundgame.mp3")

    Cell.is_game_over = False
    root = Tk()
    root.configure(bg='#555685')
    center_window(root, setup.WIDTH, setup.HEIGHT)
    root.title("Minesweeper")

    # simpan referensi ke jendela utama di dalam kelas Cell
    Cell.main_window = root

    # strict window aspect ratio
    root.resizable(False, False)

    # frame setup
    frameTop = Frame(root, bg='#EE4B2B', width=setup.WIDTH, height=utils.height_calculate(25))
    frameLeft = Frame(root, bg='#000000', width=utils.width_calculate(25), height=utils.height_calculate(75))
    frameCenter = Frame(root, bg='#4b4e96', width=utils.width_calculate(75), height=utils.height_calculate(75))

    grid_frame = Frame(frameCenter, bg='#4b4e96')  # warna sama biar nyatu
    grid_frame.place(relx=0.5, rely=0.5, anchor='center')  # PUSAT

    # Reset Cell.all dan Cell.cell_count
    Cell.all.clear()
    Cell.cell_count = setup.CELL_COUNT

    Cell.is_game_over= False # reset flag

    # cell instance
    for x in range(setup.GRID):
        for y in range(setup.GRID):
            c = Cell(x, y)
            c.create_btn_object(grid_frame)
            c.cell_btn_object.grid(column=y, row=x)

    # panggil label dari Cell class
    Cell.count_label(frameLeft)
    Cell.cell_count_label_object.place(x=0, y=0)

     # Setelah label cell_count_label_object sudah di-place, tunggu window update
    root.update_idletasks()

    # Ambil tinggi label yang sudah ada
    label_height = Cell.cell_count_label_object.winfo_height()

    # Guide Singkat
    guide_label = Label(
        frameLeft,
        width=23,
        text="📘 Guide:\nLMB = Buka Cell\nRMB = Tandai Bom",
        font=("Arial", 24),
        justify=LEFT,
        bg='#34495e',
        fg='white'
    )
    guide_label.place(x=0, y= label_height + 10)  # Geser dikit ke bawah biar ga tabrakan dengan label count
    
    #flag counter
    Cell.flag_label(frameLeft)
    Cell.flag_count_label_object.place(x=0, y=label_height + 260)


    #timer
    start_time = time.time()
    #timer (Cell)
    Cell.start_time = start_time


    timer_label = Label(
        frameLeft,
        font=("Arial", 24), 
        bg='#34495e', 
        fg='white',
        width=21,
        height=3,
        justify=LEFT
    )
    timer_label.place(x=0, y=label_height + 135)

    update_timer(timer_label, start_time)


    Cell.randomize_boms()

    judul_label = Label(
        frameTop,
        text="🧨 Minesweeper Game 🧨",
        font=("Arial", 32, "bold"),
        bg='#f44336',
        fg='white'
    )
    judul_label.place(relx=0.5, rely=0.35, anchor='center') 

    style = Style()
    style.theme_use('default')

    style.configure(
        "custom.Horizontal.TProgressbar",
        thickness=25,          
        troughcolor="#f44336", 
        background="white"     
    )

    progress = Progressbar(
        frameTop,
        orient="horizontal",
        length=1000,
        style="custom.Horizontal.TProgressbar"
    )
    progress.place(relx=0.5, rely=0.7, anchor='center')  # Di tengah bawah judul
    progress.start(1500)

    canvas = Canvas(frameTop, height=4, bg='white', highlightthickness=0)
    canvas.place(relx=0.5, rely=1.0, anchor='s', relwidth=1.0)

    # frame placement
    frameTop.place(x=0, y=0)
    frameLeft.place(x=0, y=utils.height_calculate(25))
    frameCenter.place(x=utils.width_calculate(25), y=utils.height_calculate(25))

    # run window
    root.mainloop()

def update_timer(label, start_time):
    def refresh():
        elapsed = int(time.time() - start_time)
        label.config(text=f"⏱️ Waktu: {elapsed}s")
        label.after(1000, refresh)
    refresh()

# Panggil fungsi title_screen saat program dijalankan
if __name__ == "__main__":
    title_screen()