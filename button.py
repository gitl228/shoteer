import pygame

class Button():
    def __init__(self, x ,y,w,h,text,p_image,hover_image_path = None, sound_path = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.image = pygame.transform.scale(pygame.image.load(p_image), (w,h))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.transform.scale(pygame.image.load(hover_image_path), (w,h))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.sound = None
        
    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image,self.rect.topleft)
        
        
        font = pygame.font.SysFont('Arial',36)
        text_surface = font.render(self.text, True)
        text_rect = text_surface.get_rect(centre = self.rect.center)
        screen.blit(text_surface, text_rect)
        
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    
    