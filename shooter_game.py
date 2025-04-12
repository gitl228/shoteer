from pygame import *
from random import randint
from time import time as timer
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)
 
image_folder = resource_path(".")


#Подключение
mixer.init()
font.init()

#Константы
WIDTH = 1000
HEIGHT = 600
FPS = 60
SCORE = 0
MAX_SCORE = 10
MAX_LOST = 20
BULLETS = 7

#Картинки
bg = os.path.join(image_folder, "AQAKV8rVNHdtF2TwDk3TUfy9duq8FY6pXRQDMsebYzZZdEkX58Wp5FUCUvW3xd1ill9ovJtqI8SFhZMeujDvRUU_h-s.jpg")
rocket = os.path.join(image_folder, "spp.png")
enemy = os.path.join(image_folder, "ij.png")
img_bullet = os.path.join(image_folder, 'bullet.png')
snd_back = os.path.join(image_folder, 'space.ogg')
snd_fire = os.path.join(image_folder, 'fire.ogg')
image_asteroid = os.path.join(image_folder, 'asteroid.png')

#Звуки
mixer.music.load(snd_back)
mixer.music.play()
mixer.music.set_volume(0.1)

fire_play = mixer.Sound(snd_fire)
#цвета
White = 255,255,255
gray = 150,150,150
dark_gray = 100, 100, 100
GREEN = (100,255,50)
RED = (255,100,50)

score = 0 
lost = 0 
life = 3
#Текст
font_text = font.Font(None, 36)
font_menu = font.Font(None, 36)
font_menu = font.Font(None, 70)
font_game = font.Font(None, 80)

win_text = font_game.render("EZ WIN", True, GREEN)
lose_text = font_game.render("BOT, YOU LOSE!", True, RED)

#параметры экрана
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("SHOOTER")
bg = transform.scale(image.load(bg), (WIDTH,HEIGHT))
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, p_image, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def __init__(self, p_image, x, y, w, h, speed, max_bullets):
        super().__init__(p_image,x,y,w,h,speed)
        self.max_bullets = max_bullets
        self.current_bullet = max_bullets
        
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIDTH - self.rect.width -5:
            self.rect.x += self.speed     
                     
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)
        self.current_bullet -= 1
        
    def reload(self):
        self.current_bullet = self.max_bullets
        
class AmmoIndicator(sprite.Sprite):
     def __init__(self,p_image, x,y,w,h,max_bullets):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_bullets = max_bullets
        
     def update(self,current_bullets):
         self.rect.x = WIDTH - self.rect.width - 10
         self.rect.y = HEIGHT - self.rect.height - 10
         for i in range(self.max_bullets):
             if i < current_bullets:
                 window.blit(self.image,(self.rect.x - i * (self.rect.width + 5), self.rect.y))
             
        

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - self.rect.width)
            self.rect.y = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH - self.rect.width)
            self.rect.y = 0
            lost += 1
              
class Bullet(GameSprite):
        def update(self):
            self.rect.y -= self.speed
        # Удаление пули, если она выходит за верхнюю границу экрана
            if self.rect.y < 0:
                self.kill()


player = Player(rocket, 5, HEIGHT -100, 80, 100, 7, BULLETS)
ammo_indicator = AmmoIndicator(img_bullet, WIDTH - 10, HEIGHT - 10,15,20, BULLETS)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

print(player.current_bullet,player.max_bullets)

for i in range(3):
     asteroid = Asteroid(image_asteroid, randint(0, WIDTH - 80), -40, 150, 70, randint(1, 4))
     asteroids.add(asteroid)

for i in range(6):
    monster = Enemy(enemy, randint(0, WIDTH - 80), -40, 150, 70, randint(1, 5))
    monsters.add(monster)
    
run = True
finish = False
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if player.current_bullet != 0 and not rel_time:   
                    player.fire()
                    fire_play.play()
                else:
                    last_time = timer()
                    rel_time = True    
                
    if not finish:
        window.blit(bg,(0,0))
        
        score_text = font_text.render("Счет: "+ str(score), True, White)
        window.blit(score_text, (10,20))
        
        lost_text = font_text.render("Пропущенно: "+ str(lost), True, White)
        window.blit(lost_text, (10,50))
       
        collides = sprite.groupcollide(monsters,bullets, True,True)
        for collide in collides:
            score +=1
            monster = Enemy(enemy, randint(0, WIDTH -80),-40, 150, 70, randint(1,5))
            monsters.add(monster)
        
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1
        
        if score == MAX_SCORE:
            finish = True
            window.blit(win_text,(WIDTH//2 - 150, HEIGHT//2 -50))
            mixer.music.stop()
        
        if life == 0 or lost >= MAX_LOST:
           finish = True
           window.blit(lose_text,(WIDTH//2 - 250, HEIGHT//2 -50))
           mixer.music.stop()
           
        if life == 3:
            life_color=(0,150,0)
        if life == 2:
            life_color =(150,150,0)
        if life == 1:
            life_color =(150,0,0)
            
        text_life = font_text.render("Жизни: "+ str(life), True, life_color)
        window.blit(text_life, (WIDTH // 2 + 220, 20))    
        
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        monsters.update()
        player.update()
        bullets.update()
        asteroids.update()
        ammo_indicator.update(player.current_bullet)
        
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font_text.render("ПЕРЕЗАРЯДКА...", True, RED)
                window.blit(reload_text, (WIDTH // 2 - 90, HEIGHT // 2 + 210))
            else:
                player.reload()
                rel_time = False
        
    display.update()
    clock.tick(FPS)
            