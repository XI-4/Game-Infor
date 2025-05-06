import pygame, random, time
pygame.init()

# Konfigurasi
WIDTH, HEIGHT = 400, 500
CAR_W, CAR_H = 70, 70
OBS_W, OBS_H = 25, 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Newton By IKHEN")
clock = pygame.time.Clock()

# Assets
bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
car_img = pygame.transform.scale(pygame.image.load("newton.png"), (CAR_W, CAR_H))
apple_img = pygame.transform.scale(pygame.image.load("apel.png"), (OBS_W, OBS_H))
font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 20)

# Soal fisika
questions = [
    {"question": "Apa satuan gaya dalam SI?", "options": ["A. Joule", "B. Newton", "C. Watt", "D. Pascal"], "answer": "B"},
    {"question": "Benda jatuh karena pengaruh...", "options": ["A. Gaya gesek", "B. Gaya otot", "C. Gaya gravitasi", "D. Gaya dorong"], "answer": "C"},
    {"question": "Rumus percepatan adalah...", "options": ["A. F/m", "B. m/F", "C. v*t", "D. s*t"], "answer": "A"},
    {"question": "Berapakah percepatan gravitasi di bumi?", "options": ["A. 5 m/s²", "B. 9.8 m/s²", "C. 10 m/s²", "D. 2 m/s²"], "answer": "B"},
]

def draw_text(text, font, color, surface, x, y):
    txt = font.render(text, True, color)
    surface.blit(txt, txt.get_rect(center=(x, y)))

def wait_for_key():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: return

def show_screen(title, subtitle="Tekan Spasi untuk Lanjut", color=(0, 0, 0)):
    screen.blit(bg, (0, 0))
    draw_text(title, font, color, screen, WIDTH//2, HEIGHT//2 - 50)
    draw_text(subtitle, small_font, color, screen, WIDTH//2, HEIGHT//2 + 50)
    draw_text("by Hendra dan Ikhwan", small_font, (255, 0, 0), screen, WIDTH//2, HEIGHT//3 + 50)
    pygame.display.flip()
    wait_for_key()

def ask_question():
    q = random.choice(questions)
    start = time.time()
    while True:
        if time.time() - start > 30: return False
        screen.blit(bg, (0, 0))
        draw_text("Soal Fisika!", font, (0,0,0), screen, WIDTH//2, 50)
        draw_text(q["question"], small_font, (0,0,0), screen, WIDTH//2, 120)
        for i, opt in enumerate(q["options"]):
            draw_text(opt, small_font, (0,0,0), screen, WIDTH//2, 160 + i * 30)
        draw_text("Tekan A/B/C/D", small_font, (255,0,0), screen, WIDTH//2, 300)
        draw_text(f"Waktu: {30 - int(time.time() - start)}s", small_font, (255,0,0), screen, WIDTH//2, 350)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]:
                    correct = chr(e.key).upper() == q["answer"]
                    return correct

def main_game():
    car_x, car_y = WIDTH//2, HEIGHT - CAR_W - 10
    obstacles = [{"x": random.randint(0, WIDTH - OBS_W), "y": -OBS_H}]
    score, level = 0, 1
    base_speed = 5

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()

        keys = pygame.key.get_pressed()
        car_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 10
        car_x = max(0, min(WIDTH - CAR_W, car_x))

        for o in obstacles:
            current_speed = base_speed + score // 3  # makin cepat tiap 3 skor
            o["y"] += current_speed
            if o["y"] > HEIGHT:
                o.update(y=-OBS_H, x=random.randint(0, WIDTH - OBS_W))
                score += 1
                if score % 5 == 0 and len(obstacles) < 5:  # maksimal 5 apel
                    obstacles.append({"x": random.randint(0, WIDTH - OBS_W), "y": -OBS_H})
                    level += 1

        for o in obstacles:
            if car_y < o["y"] + OBS_H and car_y + CAR_H > o["y"] and car_x < o["x"] + OBS_W and car_x + CAR_W > o["x"]:
                if ask_question():
                    obstacles.remove(o)
                    pygame.display.flip()
                    time.sleep(3)  # jeda 3 detik setelah menjawab
                    break
                else:
                    show_screen(f"Game Over! Skor: {score}", "Tekan Spasi untuk Coba Lagi", (255, 0, 0))
                    return

        screen.blit(bg, (0,0))
        screen.blit(car_img, (car_x, car_y))
        for o in obstacles: screen.blit(apple_img, (o["x"], o["y"]))
        draw_text(f"Skor: {score}", font, (0,0,0), screen, 60, 20)
        draw_text(f"Level: {level}", font, (0,0,0), screen, 60, 50)
        pygame.display.flip()
        clock.tick(30)

# Main
show_screen("Game Newton's Apple")
while True:
    main_game()
