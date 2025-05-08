import pygame
import random

# Inisialisasi
pygame.init()
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat Jump v2")

# Load gambar kucing
cat_img = pygame.image.load("cat.png")
cat_img = pygame.transform.scale(cat_img, (50, 50))

# Load suara
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
except:
    jump_sound = None

# Warna
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLUE = (135, 206, 250)

clock = pygame.time.Clock()

# Karakter
cat = pygame.Rect(200, 500, 50, 50)
cat_vel_y = 0
gravity = 0.5
jump_strength = -12

# Platform
platforms = []

# Skor
score = 0
high_score = 0
platform_speed_multiplier = 1  # Kecepatan platform bertambah tiap skor 20

# Chaos mode & musuh
chaos_mode = False
enemy = None
enemy_speed = 4

def reset_game():
    global cat, cat_vel_y, platforms, score, chaos_mode, enemy, platform_speed_multiplier
    cat.x, cat.y = 200, 500
    cat_vel_y = 0
    score = 0
    chaos_mode = False
    enemy = None
    platform_speed_multiplier = 1
    platforms = []

    base_rect = pygame.Rect(150, 550, 100, 10)
    platforms.append({"rect": base_rect, "vel": 0, "x_float": float(base_rect.x)})

    y = 450
    for _ in range(9):
        w = random.randint(80, 120)
        x = random.randint(0, WIDTH - w)
        rect = pygame.Rect(x, y, w, 10)
        vel = random.choice([-0.5, 0.5])
        platforms.append({"rect": rect, "vel": vel, "x_float": float(x)})
        y -= 100

# Game loop
running = True
game_over = False
reset_game()

while running:
    clock.tick(60)

    if chaos_mode:
        win.fill((20, 20, 30))
    else:
        win.fill((BLUE[0], BLUE[1] - score % 100, BLUE[2]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if not chaos_mode and score >= 15:
            chaos_mode = True
            enemy = pygame.Rect(random.randint(0, WIDTH - 40), -60, 40, 40)

        if keys[pygame.K_LEFT]:
            cat.x -= 5
        if keys[pygame.K_RIGHT]:
            cat.x += 5

        if cat.x < -50:
            cat.x = WIDTH
        if cat.x > WIDTH:
            cat.x = -50

        cat_vel_y += gravity
        cat.y += cat_vel_y

        for plat in platforms:
            if cat.colliderect(plat["rect"]) and cat_vel_y > 0:
                cat_vel_y = jump_strength
                score += 1
                if jump_sound:
                    jump_sound.play()

                # Update kecepatan platform setiap kelipatan 20 skor
                if score % 20 == 0:
                    platform_speed_multiplier = 1 + (score // 20) * 0.2
                    for p in platforms:
                        if p["vel"] != 0:
                            p["vel"] = 0.5 * platform_speed_multiplier if p["vel"] > 0 else -0.5 * platform_speed_multiplier

        if cat.y < HEIGHT / 2:
            offset = abs(cat_vel_y)
            cat.y = HEIGHT / 2
            for plat in platforms:
                plat["rect"].y += offset
            if chaos_mode and enemy:
                enemy.y += offset
            while len(platforms) < 10:
                w = random.randint(80, 120)
                x = random.randint(0, WIDTH - w)
                y = platforms[-1]["rect"].y - 100
                vel = random.choice([-0.5, 0.5])
                vel *= platform_speed_multiplier  # Terapkan multiplier ke platform baru
                rect = pygame.Rect(x, y, w, 10)
                platforms.append({"rect": rect, "vel": vel, "x_float": float(x)})

        for plat in platforms:
            plat["x_float"] += plat["vel"]
            plat["rect"].x = int(plat["x_float"])
            if plat["rect"].left <= 0 or plat["rect"].right >= WIDTH:
                plat["vel"] *= -1

        platforms = [p for p in platforms if p["rect"].y < HEIGHT + 50]

        for plat in platforms:
            color = (180, 0, 0) if chaos_mode else GREEN
            pygame.draw.rect(win, color, plat["rect"])

        if chaos_mode and enemy:
            enemy.y += enemy_speed
            pygame.draw.rect(win, (200, 50, 50), enemy)

            if enemy.y > HEIGHT:
                enemy.x = random.randint(0, WIDTH - enemy.width)
                enemy.y = -60

            if cat.colliderect(enemy):
                game_over = True

        win.blit(cat_img, (cat.x, cat.y))

        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Skor: {score}", True, (0, 0, 0))
        win.blit(score_text, (10, 10))

        if cat.y > HEIGHT:
            game_over = True
            if score > high_score:
                high_score = score

    else:
        font = pygame.font.SysFont("Arial", 24)
        font_big = pygame.font.SysFont("Arial", 32, bold=True)
        game_over_text = font_big.render("Game Over!", True, (255, 0, 0))
        win.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        restart_text = font.render("Tekan [R] untuk main lagi", True, (0, 0, 0))
        win.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2))
        high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
        win.blit(high_score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 30))

        if keys[pygame.K_r]:
            game_over = False
            reset_game()

    pygame.display.update()

pygame.quit()
