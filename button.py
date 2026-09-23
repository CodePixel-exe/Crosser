import pygame
from resource_path import file_path

pygame.mixer.init()

#This will allow my main code to have much less lines as I can import this class as a module
#button class will allow buttons to be styled
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        #loads sound for menu
        self.click_sound = pygame.mixer.Sound(file_path("sounds/clicksound.wav"))
    
    #function allows for button interaction
    def draw(self, surface):
        #action is set to False when the mouse hasn't been clicked
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked condition
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]  == 1 and self.clicked == False:
            #changes to True because the button was clicked the left mouse button
                    self.clicked = True
                    action = True
                    self.click_sound.play()#plays when button is clicked
       
        #detects if the left mouse button is clicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draws buttons on screen
        surface.blit(self.image,(self.rect.x, self.rect.y))
        
        #passes back the action variable
        return action

