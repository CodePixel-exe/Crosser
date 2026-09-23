#SHOP PROGRAM
#Buy powerups and lives

#Imports for game functionality
import pygame, button, sys, os
#Import to wrap sprites and assets for later compiling
from resource_path import file_path
import menu

#Initialise the pygame module and allow it to be used
pygame.init()

#Dimensions for the window.
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

#sets the display mode to the screen measurements.
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
#Sets the title of the window
pygame.display.set_caption("Crosser Shop")

#sets the menu state to shop when on the shop menu.
menu_state = "shop"

class shopElements:
    def itemButtons():
        pass
    
    #title for main menu
def title():
    #font for the title
    font = pygame.font.Font(file_path("font/doctorglitch.otf"), 115)
    #text that will be displayed in the title
    text = font.render("Shop", True, (255,255,255))
    #creates rectangular object for text to be drawn on
    textRect = text.get_rect()
    #centers text horizontally
    textRect.centerx = SCREEN_WIDTH // 2
    #ensures the title is 20 pixels away from the top
    textRect.top = 20
    #returns variables so that they can be used in the main game loop
    return text, textRect


text, textRect = title()

#draw text function allows for the GUI to display text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

 #loop for menu
run = True
while run:
    #colour of background.
    screen.fill((135,206,250))
    screen.blit(text, textRect)
    pygame.draw.rect(screen, (255, 255, 255), (40, 160, 730, 420), width = 20)

     #Events handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
#calls the quit function  
pygame.quit()








