#imports pygame library
import pygame, time
#imports the button class to make use of it in this program
import button
#imports the os library to open the game file
import os
#allows pygame module to run
pygame.init()

#Width and height for the game window that will be created
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#text for window
pygame.display.set_caption("Main Menu")

pygame.mixer.init()
#menu variables for menu states and accessing different menus
menu_state = "main"

#title for main menu
def title():
    #font for the title
    font = pygame.font.Font("font/doctorglitch.otf", 115)
    #text that will be displayed in the title
    text = font.render("Crosser", True, (255,255,255))
    #creates rectangular object for text to be drawn on
    textRect = text.get_rect()
    #centers text horizontally
    textRect.centerx = SCREEN_WIDTH // 2
    #ensures the title is 20 pixels away from the top
    textRect.top = 20
    #returns variables so that they can be used in the main game loop
    return text, textRect

#calls title function
text, textRect = title()

#load buttons
start_img = pygame.image.load("graphics/start.png").convert_alpha()
options_img = pygame.image.load("graphics/options.png").convert_alpha()
exit_img = pygame.image.load("graphics/exit.png").convert_alpha()
tutorial_img = pygame.image.load("graphics/tutorial.png").convert_alpha()
back_img = pygame.image.load("graphics/back.png").convert_alpha()
controls_img = pygame.image.load("graphics/controls.png").convert_alpha()

#load sprite images for tutorial menu
pedestrian_img = pygame.image.load("sprites/Ped v2.png").convert_alpha()
ped_display = button.Button(550, 450, pedestrian_img, 2)
coin_img = pygame.image.load("sprites/coin V2.png")
coin_display = button.Button(550, 360, coin_img, 2)


#create button instances
#start button
start_button = button.Button(290, 200, start_img, 0.7)
#options button
options_button = button.Button(290, 330, options_img, 0.7)
#exit button
exit_button = button.Button(290, 450, exit_img, 0.7)
#controls button
controls_button = button.Button(290, 200, controls_img, 0.7)
#tutorial button
tutorial_button = button.Button(290, 410, tutorial_img, 0.7)
#back button
back_button = button.Button(70, 480, back_img, 0.5)

#draw text function allows for the GUI to display text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

#main menu functions 
def main_menu():
    if start_button.draw(screen): #checks if button is clicked
        os.system("crosser.py")
    if options_button.draw(screen):
        return "options"
    if exit_button.draw(screen):
        return "exit"
    return "main"

#options menu functions
def options_Menu():
    if controls_button.draw(screen):
        return "controls"
    if tutorial_button.draw(screen):
        return "tutorial"
    if back_button.draw(screen):
        return "main"
    return "options"

#this menu displays the controls to the user
def controls_menu():
    #font for text
    font = pygame.font.Font(None,40)
    draw_text("Controls: Use Arrow Keys to move:", font,(255,255,255), 200, 255)
    draw_text("Up Arrow = Move Forward", font,(255,255,255), 200, 290)
    draw_text("Left Arrow = Move Left", font,(255,255,255), 200, 320)
    draw_text("Right Arrow = Move Right", font,(255,255,255), 200, 350)
    if back_button.draw(screen):
        return "options"
    return "controls"

#this menu will tell you the main objective of the game
def tutorial_menu():
    font = pygame.font.Font(None,27)
    draw_text("Crosser is a game where you play as a car and score points for every move!", font,(255,255,255), 70, 255)
    draw_text("You also can score points with coins too! They give you 10 points per coin.", font,(255,255,255), 70, 285)
    draw_text("But watch out for the Pedestrians! If you hit them it's game over!", font,(255,255,255), 70, 315)
    draw_text("Pedestrian:", font,(255,255,255), 400, 470)
    draw_text("Coin:", font,(255,255,255), 400, 390)
    textRect.centerx = SCREEN_WIDTH // 2 
    ped_display.draw(screen)
    coin_display.draw(screen)  
    if back_button.draw(screen):
        return "options"
    return "tutorial"

#music.play(-1)

#loop for menu
run = True
while run:
    screen.fill((135,206,250))
    screen.blit(text, textRect)
    pygame.draw.rect(screen, (255, 255, 255), (40, 160, 730, 420), width = 20)
    if menu_state == "main":
        menu_state = main_menu()
    elif menu_state == "options":
        menu_state = options_Menu()
    elif menu_state == "controls":
        menu_state = controls_menu()
    elif menu_state == "tutorial":
       menu_state = tutorial_menu()
    elif menu_state == "exit":
        run = False
   
    #Events handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
#calls the quit function  
pygame.quit()
