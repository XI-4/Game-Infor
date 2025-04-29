
import pygame, sys, time, os

# Kesulitan
difficulty = 25

# Window size
frameX = 720
frameY = 480

# os.system()
html = '''
mshta "about:<script>var jawab = confirm('Yakin mau main? (HANYA BISA SEKALI)');var fso = new ActiveXObject('Scripting.FileSystemObject');var file = fso.CreateTextFile('confirm.txt', true);file.Write(jawab ? 'yes' : 'no'); file.Close(); close();</script>"
'''
# 2. Jalankan popup
os.system(html)

try:
    with open('confirm.txt', 'r') as f:
        result = f.read().strip()
    os.remove('confirm.txt')
except:
    result = 'no'
    
if result == 'no':
    sys.exit(-1)

# Checks for errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] {check_errors[1]} errors, exiting...')
    sys.exit(-1)
else:
    print('[+] Berhasil')

# Inisialisasi game Window
pygame.display.set_caption('JÖRMEINGANDR')
gameDisplay = pygame.display.set_mode((frameX, frameY))

# Set Color Variable
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
button_color = pygame.Color(70, 70, 70)
button_hover = pygame.Color(100, 100, 100)


# Game variables
def reset_game():
    global snakePos, snakeRil, direction, change, score, waktuTumbuhTerakhir, startDifficulty, game_active, jedaTumbuh, difficulty
    snakePos = [100, 50]
    snakeRil = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    direction = 'RIGHT'
    change = direction
    score = 0
    jedaTumbuh = 0.1
    waktuTumbuhTerakhir = time.time()
    startDifficulty = 25
    difficulty = 25
    game_active = True
    pygame.mixer.music.load("musics.mp3")
    pygame.mixer.music.play(-1)

reset_game()

# Button
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        
    def show(self, surface):
        color = button_hover if self.is_hovered else button_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, white, self.rect, 2)
        
        font = pygame.font.SysFont('consolas', 20)
        textDIsplay = font.render(self.text, True, white)
        textRect = textDIsplay.get_rect(center=self.rect.center)
        surface.blit(textDIsplay, textRect)
        
    def kena(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.action:
                self.action()

def brutal():
    for i in range(5):
        os.system(f'start "" mshta "about:<script>document.title=\'Motivasi #{i+1}\';alert(\'For I consider that the sufferings of this present time are not worth comparing with the glory that is to be revealed to us. (Romans 8:18)\');close();</script>"')
        time.sleep(0.1)
    os.system("echo 'Dan janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya tidak ada yang berputus asa dari rahmat Allah, melainkan kaum yang kafir. (QS. Yusuf: 87)' > loser.txt | notepad loser.txt")
    os.system("del loser.txt")
    os.system("start chrome https://indopsycare.com/suicide-prevention/ | start chrome https://www.youtube.com/watch?v=S4Mry3grJS4 ")
    os.system("p")

def popAp():
    os.system("powershell -Command \"Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('For I consider that the sufferings of this present time are not worth comparing with the glory that is to be revealed to us. (Romans 8:18)', 'Looser', 'OK', 'Info')\"")
# Create buttons
restart = Button(frameX//2 - 150, frameY//2 + 60, 120, 40, "Restart", reset_game)
quit = Button(frameX//2 + 30, frameY//2 + 60, 120, 40, "Quit", popAp)

# Game Over
def gameOver():
    global game_active
    game_active = False
    
    setFont = pygame.font.SysFont('times new roman', 90)
    gameOverDisplay = setFont.render('MATI', True, red)
    gameOverRect = gameOverDisplay.get_rect()
    gameOverRect.midtop = (frameX/2, frameY/4)
    
    scoreFont = pygame.font.SysFont('times new roman', 40)
    scoreDisplay = scoreFont.render(f'Final Score: {score}', True, white)
    scoreRect = scoreDisplay.get_rect()
    scoreRect.midtop = (frameX/2, frameY/2)
    
    gameDisplay.fill(black)
    gameDisplay.blit(gameOverDisplay, gameOverRect)
    gameDisplay.blit(scoreDisplay, scoreRect)
    
    # SHow button
    restart.show(gameDisplay)
    quit.show(gameDisplay)
    pygame.mixer.music.stop()
    pygame.display.flip()

# Score
def show_score(choice, color, font, size):
    scoreFont = pygame.font.SysFont(font, size)
    scoreDisplay = scoreFont.render('Score : ' + str(score) + ' | Speed: ' + str(difficulty), True, color)
    scoreRect = scoreDisplay.get_rect()
    if choice == 1:
        scoreRect.midtop = (frameX/2, 15)
    else:
        scoreRect.midtop = (frameX/2, frameY/1.25)
    gameDisplay.blit(scoreDisplay, scoreRect)

# Main game loop
running = True
game_active = True
pygame.mixer.music.load("musics.mp3")
pygame.mixer.music.play()
while running:
    mousePos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            brutal()
            running = False
            
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    running = False
        else:
            restart.kena(mousePos)
            quit.kena(mousePos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                restart.handle_event(event)
                quit.handle_event(event)
    if game_active:
        
        # biar ga nabrak
        if change == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # menggerakkan ulaar
        if direction == 'UP':
            snakePos[1] -= 10
        if direction == 'DOWN':
            snakePos[1] += 10
        if direction == 'LEFT':
            snakePos[0] -= 10
        if direction == 'RIGHT':
            snakePos[0] += 10

        # Mekanisme Pertumbuhan Ular
        skrng = time.time()
        if skrng - waktuTumbuhTerakhir >= jedaTumbuh:
            score += 1
            if score % 10 == 0:
                # Ngeset Speed (nambah 1 tiap 10 score)
                difficulty = startDifficulty + (score // 10)
            waktuTumbuhTerakhir = skrng
        else:
            snakeRil.pop()
        
        snakeRil.insert(0, list(snakePos))

        # GFX
        gameDisplay.fill(black)
        for pos in snakeRil:
            pygame.draw.rect(gameDisplay, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Limit frame
        if snakePos[0] < 0:
            snakePos[0] = frameX - 10
        if snakePos[0] >= frameX:
            snakePos[0] = 0
        if snakePos[1] < 0:
            snakePos[1] = frameY - 10
        if snakePos[1] >= frameY:
            snakePos[1] = 0
        # Game Over conditions
        for block in snakeRil[1:]:
            if snakePos[0] == block[0] and snakePos[1] == block[1]:
                gameOver()

        show_score(1, white, 'consolas', 20)
    else:
        restart.kena(mousePos)
        quit.kena(mousePos)
    
    pygame.display.update()
    pygame.time.Clock().tick(difficulty)

pygame.quit()
sys.exit()