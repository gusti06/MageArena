import pygame
import random
import time
from abc import ABC, abstractmethod

# Inisialisasi pygame (tampilan layar game)
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Of Heroes")

# Warna dasar didalam game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock() #kecepatan didalam game
font = pygame.font.SysFont(None, 30) #font game 30

# Musik latar
pygame.mixer.music.load("Sound.mp3.mp3") #backshound
pygame.mixer.music.play(-1)   #-1 karna bisa diulang2 lagunya(klo 0 hanya sekali pemutaran)

# Efek suara
ice_sound = pygame.mixer.Sound("Air sound.mp3")
light_sound = pygame.mixer.Sound("light sound.mp3")
fire_sound = pygame.mixer.Sound("api sound.mp3")

# Gambar
background_image = pygame.image.load("ingame.png").convert()
menu_background = pygame.image.load("menu.png").convert()
player_image = pygame.image.load("main.png").convert_alpha()
enemy_image = pygame.image.load("goblin.png").convert_alpha()
ice_image = pygame.image.load("ice.png").convert_alpha()
lightning_image = pygame.image.load("light.png").convert_alpha()
fireball_image = pygame.image.load("fireball.png").convert_alpha()

# Posisi awal pemain
player_rect = player_image.get_rect()
player_rect.topleft = (100, HEIGHT // 2)

#-----------------------------------------------
# --- Abstraction(abstraksi) & Encapsulation --- 
#-----------------------------------------------
class Projectile(ABC):  # Abstraction: Class abstrak sebagai blueprint peluru  (seperti Fireball, Ice, Lightning)
    def __init__(self, x, y, speed):  # Encapsulation: Mengemas data posisi & kecepatan
        self.rect = pygame.Rect(x, y, 32, 32)
        self.speed = speed

    def update(self):  # Encapsulation: Mengatur logika pergerakan peluru Menyembunyikan detail internal peluru seperti posisi (self.rect) dan kecepatan (self.speed) dalam satu objek.
        self.rect.x += self.speed

    @abstractmethod
    def draw(self, surface):  # Abstraction: Method abstrak untuk menggambar peluru
        pass

    def type(self):  # Encapsulation: Mengembalikan jenis peluru berdasarkan kelas
        return self.__class__.__name__

#-------------------------------------------------------------
# --- Inheritance(pewarisan) & Polymorphism(banyak bentuk) ---
#-------------------------------------------------------------
class Fireball(Projectile):  # Inheritance dari Projectile (kelas ini mewarisi semua atribut dan metode dari Projectile.)
    def draw(self, surface):  # Polymorphism: Implementasi spesifik gambar Fireball
        surface.blit(fireball_image, self.rect.topleft) #^Fungsi draw() ini dipanggil di bagian utama game secara umum tanpa perlu tahu jenis peluru (contoh: proj.draw(win)).

class Ice(Projectile):  # Inheritance dari Projectile (Artinya mereka tidak perlu lagi menuliskan kode seperti update(), __init(), atau type(), karena sudah tersedia di superclass Projectile.)
    def draw(self, surface):  # Polymorphism: Implementasi spesifik gambar Ice
        surface.blit(ice_image, self.rect.topleft)#Fungsi draw() ini dipanggil di bagian utama game secara umum tanpa perlu tahu jenis peluru (contoh: proj.draw(win)).

class Lightning(Projectile):  # Inheritance dari Projectile
    def draw(self, surface):  # Polymorphism: Implementasi spesifik gambar Lightning
        surface.blit(lightning_image, self.rect.topleft)

# Variabel status game
player_hp = 100
cooldowns = {"ice": 0, "lightning": 0}
cooldown_time = {"ice": 3, "lightning": 5}
projectiles = []
enemies = []
score = 0
level = 1
fireball_speed = 7

def spawn_enemy():  # Fungsi untuk menambahkan musuh secara acak
    y = random.randint(50, HEIGHT - 50)
    enemies.append(pygame.Rect(WIDTH, y, 40, 40))
#---------------------------------------------------------
# Polymorphism: draw akan sesuai dengan jenis proyektil---
#---------------------------------------------------------
def draw():  # Menggambar semua elemenz permainan ke layar (Menampilkan Semua Elemen ke Layar)
    win.blit(background_image, (0, 0))
    win.blit(player_image, player_rect)
    for proj in projectiles:
        proj.draw(win)  # Polymorphism: draw akan sesuai dengan jenis proyektil
    for e in enemies:
        win.blit(enemy_image, e.topleft)
    pygame.draw.rect(win, RED, (10, 10, player_hp * 2, 20))
    win.blit(font.render(f'HP: {player_hp}', True, WHITE), (10, 35))
    win.blit(font.render(f'Score: {score}', True, WHITE), (WIDTH - 150, 10))
    win.blit(font.render(f'Level: {level}', True, WHITE), (WIDTH - 150, 35))
    pygame.display.update()

def update_projectiles():  # Update posisi proyektil dan cek tabrakan dengan musuh
    global enemies, score
    for proj in projectiles[:]:
        proj.update()
        for enemy in enemies[:]:
            if proj.rect.colliderect(enemy):
                enemies.remove(enemy)
                score += 1
                if proj.type() not in ("Ice", "Lightning"):
                    projectiles.remove(proj)
                break
        if proj.rect.x > WIDTH:
            projectiles.remove(proj)

def update_enemies():  # Update posisi musuh dan cek tabrakan dengan pemain
    global player_hp
    for e in enemies[:]:
        e.x -= 2
        if e.colliderect(player_rect):
            enemies.remove(e)
            player_hp -= 10
        elif e.x < 0:
            enemies.remove(e)
            player_hp -= 5

def game_over():  # Menampilkan layar game over
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Sound game over.mp3")
    pygame.mixer.music.play(-1)
    while True:
        win.fill(BLACK)
        msg = font.render("Game Over", True, WHITE)
        final_score = font.render(f"Final Score: {score}", True, WHITE)
        prompt = font.render("Press Enter to return to Menu or ESC to Quit", True, WHITE)
        win.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))
        win.blit(final_score, (WIDTH//2 - final_score.get_width()//2, 250))
        win.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Sound.mp3.mp3")
                    pygame.mixer.music.play(-1)
                    return "menu"
                elif event.key == pygame.K_ESCAPE:
                    return "exit"

def show_menu():  # Menampilkan menu utama
    selected = 0
    options = ["Start", "Info", "Exit"]
    showing_info = False
    while True:
        win.blit(menu_background, (0, 0))
        if showing_info:
            info_lines = [
                "Created by: Kelompok 2 PBO RA",
                "1. Doni Agus Setiawan",
                "2. Aprililianti",
                "3. Nabila Ramadhani Mujahidin",
                "4. Yuni Okta Safitri",
                "Controls:",
                "  ↑/↓ = Move",
                "  Z = Fireball",
                "  X = Ice",
                "  C = Lightning",
                "  ESC = Exit",
                "Press ESC to go back."
            ]
            for i, line in enumerate(info_lines):
                win.blit(font.render(line, True, WHITE), (200, 250 + i*30))
        else:
            for i, option in enumerate(options):
                color = YELLOW if i == selected else WHITE
                win.blit(font.render(option, True, color), (WIDTH//2 - 50, 250 + i*40))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if showing_info and event.key == pygame.K_ESCAPE:
                    showing_info = False
                elif not showing_info:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if options[selected] == "Start": return "start"
                        if options[selected] == "Info": showing_info = True
                        if options[selected] == "Exit": return "exit"

# Game loop utama
while True:
    choice = show_menu()
    if choice == "exit":
        break
    if choice == "start":
        # Reset variabel game
        player_hp = 100
        projectiles = []
        enemies = []
        score = 0
        level = 1
        fireball_speed = 7
        cooldown_time = {"ice": 3, "lightning": 5}
        player_rect.topleft = (100, HEIGHT//2)

        pygame.mixer.music.stop()
        pygame.mixer.music.load("Sound.mp3.mp3")
        pygame.mixer.music.play(-1)

        last_spawn = time.time()
        last_fireball = 0
        fireball_delay = 0.15
        running = True

        while running:
            clock.tick(60)
            draw()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]: player_rect.y -= 5
            if keys[pygame.K_DOWN]: player_rect.y += 5
            player_rect.clamp_ip(win.get_rect())

            now = time.time()
            if now - last_spawn > 1:
                spawn_enemy()
                last_spawn = now

            update_projectiles()
            update_enemies()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_z and now - last_fireball > fireball_delay:
                        last_fireball = now
                        projectiles.append(Fireball(player_rect.x+40, player_rect.y+10, fireball_speed))
                        fire_sound.play()
                    if event.key == pygame.K_x and now - cooldowns["ice"] > cooldown_time["ice"]:
                        cooldowns["ice"] = now
                        projectiles.append(Ice(player_rect.x+40, player_rect.y+10, 5))
                        ice_sound.play()
                    if event.key == pygame.K_c and now - cooldowns["lightning"] > cooldown_time["lightning"]:
                        cooldowns["lightning"] = now
                        projectiles.append(Lightning(player_rect.x+40, player_rect.y+10, 6))
                        light_sound.play()

            if score // 10 + 1 > level:
                level += 1
                fireball_speed += 1
                cooldown_time["ice"] = max(1, cooldown_time["ice"] - 0.2)
                cooldown_time["lightning"] = max(2, cooldown_time["lightning"] - 0.2)

            if player_hp <= 0:
                result = game_over()
                if result == "exit":
                    pygame.quit()
                    exit()
                if result == "menu":
                    break

pygame.quit()





#Polymorphism Dinamis (Dynamic Polymorphism) menggunakan pewarisan dan metode override.
#