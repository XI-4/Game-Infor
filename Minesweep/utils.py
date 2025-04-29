# MultipleFiles/utils.py
import setup
import tkinter

def height_calculate(percentage):
    return (setup.HEIGHT / 100) * percentage

def width_calculate(percentage):
    return (setup.WIDTH / 100) * percentage

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int((screen_width - width) / 2)
    center_y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{center_x}+{center_y}")