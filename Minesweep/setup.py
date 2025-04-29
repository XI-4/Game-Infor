# MultipleFiles/setup.py
WIDTH = 1600
HEIGHT = 900

# Variabel untuk tingkat kesulitan
DIFFICULTY = 'medium'  # Pilihan: 'easy', 'medium', 'hard'

# Pengaturan default
GRID = 6
BOM = 6
CELL_COUNT = GRID ** 2

def update_settings(difficulty):
    global GRID, BOM, CELL_COUNT
    if difficulty == 'easy':
        GRID = 5
        BOM = 5     
    elif difficulty == 'medium':
        GRID = 6
        BOM = 7  
    elif difficulty == 'hard':
        GRID = 8
        BOM = 12 
    CELL_COUNT = GRID ** 2  # Update CELL_COUNT sesuai GRID