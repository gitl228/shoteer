import pygame
import sys 
from button import Button

pygame.init()
win_width = 960
win_height = 600
FPS = 60
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Menu')
bg = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (960,600))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

def main_menu():
    start_btn = Button(win_width/2 -(252/2), 150,252,74, 'Начать игру', 'pngtree-game-button-technology-button-colorful-technology-button-source-file-start-button-png-image_462025.png', 'sounds/button.ogg')
    
    run = True
    while run:
        screen.fiil((0,0,0))
        screen.blit(bg, (0,0))
        font = pygame.font.SysFont('Arial',72)
        text_surface = font.render('Menu', True, (255,255,255))
        text_rect = text_surface.getrect(center = (win_width/2,100))
        screen.blit(text_surface,text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit
        if event.type == pygame.USEREVENT and event.button == start_btn:
            new_game()
            
            run = False
            sys.exit()
        for btn in [start_btn]:
            btn.handle_event(event)
        for btn in [start_btn]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
            
       