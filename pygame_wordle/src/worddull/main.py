from typing import List, Dict, Tuple
from color_palette import get_rgb
import pygame
import db_funcs

# initialize and prepare screen dimensions
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 844
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#init rectangle
bg_letter_all = pygame.Rect((300,250,50,50))
bg_letter_doesnt_occur = pygame.Rect((500,600,50,50))
bg_letter_occurs_correct_spot = pygame.Rect((400,100,50,50))
bg_letter_occurs_wrong_spot = pygame.Rect((600,500,50,50))
run = True
while run:
    screen.fill(color=get_rgb('background'))
    pygame.draw.rect(surface=screen, color=get_rgb('blue'), rect=bg_letter_all)
    pygame.draw.rect(surface=screen, color=get_rgb('red'), rect=bg_letter_doesnt_occur)
    pygame.draw.rect(surface=screen, color=get_rgb('green'), rect=bg_letter_occurs_correct_spot)
    pygame.draw.rect(surface=screen, color=get_rgb('yellow'), rect=bg_letter_occurs_wrong_spot)
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()