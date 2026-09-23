import pygame, random
import sys, os
#imports the pedestrian class in the game folder to be used in the main game file
from ped import PedSprite

def file_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS,relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#height and width
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
#scroll threshhold to enable scrolling
SCROLL_THRESH = 150

#Game variables
TILE_SIZE = 64

#establishes how many coins are allowed to spawn.
COIN_COUNT = 5

#Main game initilisation
pygame.init()

#initialises the sound commands
pygame.mixer.init()
  
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#text for window
pygame.display.set_caption("Crosser")
clock = pygame.time.Clock()

#sprites and graphics
path_image = pygame.image.load(file_path("graphics/path.png")).convert_alpha()
coin = pygame.image.load(file_path("sprites/coin V2.png")).convert_alpha()

#Car class for all of the functions relating to the car
class CAR:
    def __init__(self, x, y, scale):
        #loads in car sprite#
        self.car = pygame.image.load(file_path("sprites/car.png")).convert_alpha()
        width, height = self.car.get_size()
        #allows for scaling of the sprite
        self.car = pygame.transform.scale(self.car,(int(width*scale),int(height*scale)))
        #gets the rectangle for the car so it can establish a surface for the sprite to be drawn on
        self.rect = self.car.get_rect(topleft = (x,y))
        width, height = self.car.get_size()
        #ensures x and y positions are stored as whole numbers rather than floats (easier to calcluate position)
        self.x = int(x)
        self.y = int(y)
    
    #draws the car sprite
    def draw_car(self,screen):
       screen.blit(self.car, (self.x, self.y))
    
    #updates the cars rectangle when moving
    def update_car(self, dy, dx):
        self.rect.x += dx
        self.rect.y += dy

    #allows for the car to move
    def move_car(self, dx, dy, move_x, move_y):
        self.x += dx * move_x
        self.y += dy * move_y
        #establishes the dimensions of the player sprite
        self.rect = pygame.Rect(self.x, self.y, self.car.get_width(), self.car.get_height())
    
   


#paths
class PATHS(pygame.sprite.Sprite):
    #allows for the path sprites to be resized 
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(path_image, (int(width), int(height)))
        #calls the sprite to be drawn
        self.rect = self.image.get_rect()
        #establishes the x and y coordinate variables for paths
        self.rect.x = x
        self.rect.y = y
    
    def update(self, scroll):
        self.rect.y += scroll

    def draw_path(self):
        screen.blit(self.image,(self.rect.x, self.rect.y))  

#Coins
class COIN:
    #initilaises coins and passes cell width and cell height args
    def __init__(self, cell_width, cell_height):
        self.cell_width = cell_width
        self.cell_height = cell_height
        #calculates the size of cell that the sprite spawns in
        size = int(min(cell_width,cell_height)*0.8)
        #allows for scaling of the coin sprite
        self.coin = pygame.transform.scale(coin, (size,size))
        self.size = size
        self.pos = pygame.math.Vector2(0,0)
        self.update_rect()
    
    #updates the coins surface that the image will be drawn on.
    def update_rect(self):
        self.rect = pygame.Rect(int(self.pos.x),int(self.pos.y),self.size,self.size)
    
    #allows for coin rect to be drawn
    def draw_coin(self):
        screen.blit(self.coin, self.rect)
    
    #allows coins to be randomised
    def randomize(self):
     while True:
        #calculates the grid for the coins spawning
        total_cells_x = SCREEN_WIDTH // self.cell_width
        total_cells_y = SCREEN_HEIGHT // self.cell_height
        
        #odd collumns and rows (roads)
        col = random.randrange(1, total_cells_x, 2)
        row = random.randrange(1, total_cells_y, 2)
        
        #calcuate position
        x = col * self.cell_width
        y = row * self.cell_height
        
        #centers coins in road
        centered_x = x + (self.cell_width - self.size) // 2
        centered_y = y + (self.cell_height - self.size) // 2
        
        #Establishes the position variable for the distance between coins
        self.pos = pygame.math.Vector2(centered_x, centered_y)
        self.update_rect()
        break
    
#peds class to establish the pedestrian element
class PEDS(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, ped_sprite, scale, direction ="right"):
        #initilises the base class for the pedestian object
        pygame.sprite.Sprite.__init__(self)
        #allows for scaling and utilises a class from another pygame file
        image = ped_sprite.get_image(0, 32,30, scale)
        self.image = image
        self.rect = self.image.get_rect(topleft=(0 if direction == "right" else SCREEN_WIDTH, y))
        self.direction = direction
        
        #allows for left right movement with the pedestrians
        if self.direction == "right":
            self.rect.x = self.rect.width
        else:
            self.rect.x = SCREEN_WIDTH

        self.rect.y = y
    
    #draws the rectangle for the pedestrian
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    #function to allow pedestrians to go left and right and also set their speed.
    def update(self):
        speed = 2
        if self.direction == "right":
            self.rect.x += speed
            if self.rect.x > SCREEN_WIDTH:
                self.rect.x = -self.rect.width
        else:
            self.rect.x -= speed
            if self.rect.right < 0:
                self.rect.x = SCREEN_WIDTH
        
#this will contain some main game elements like checking for collisions
class MAIN:
    def __init__(self):
        self.ped_group = PedSprite()
        self.world_row_Os = 0
        #ped collision sound
        self.hit_sound = pygame.mixer.Sound(file_path("sounds/hit.mp3"))
        #font for game elements like the score
        self.game_font = pygame.font.Font(file_path("font/doctorglitch.otf"), 96)
        self.score_font = pygame.font.Font(file_path("font/doctorglitch.otf"), 22)
        self.ui_font = pygame.font.Font(file_path("font/doctorglitch.otf"), 22)
        #Coin sound#
        self.coin_sound = pygame.mixer.Sound(file_path("sounds/coin_collect.wav"))
        self.paths = []# List for paths to be appended to
        paths = 4 #Paths per row
        total_cells = paths * 2 - 1
        #calculates grid dimensions for paths
        self.cell_height = SCREEN_HEIGHT // total_cells
        self.cell_width = SCREEN_WIDTH // total_cells
        
        #scrolling and score variables
        self.score = 0
        self.hi_score = 0
        self.scroll_targ = 0
        self.scroll_speed = 4
        
        #list for coins to be appended to.
        self.coin = []
        #tracks used positions to prevent coins overlapping
        self.used_positions = set()
        #calculatees grid  dimensions for coins
        self.total_cells_x = SCREEN_WIDTH // self.cell_width
        self.total_cells_y = SCREEN_HEIGHT // self.cell_height
        
        #for loop based on the amount of coins in coin count.
        for _ in range(COIN_COUNT):
            #attempts variable to check for coins attempting to be placed in odd rows and columns
            attempts = 0
            while attempts <= 100:
                #randomly positions them with the randrange command via the cells
                col = random.randrange(1, self.total_cells_x, 2)
                row = random.randrange(1, self.total_cells_y, 2)
                if (col, row) not in self.used_positions:
                    self.used_positions.add((col, row))
                    x = col * self.cell_width
                    y = row * self.cell_height
                    #centers coin in cell
                    centered_x = x + (self.cell_width - TILE_SIZE) // 2
                    centered_y = y + (self.cell_height - TILE_SIZE) // 2
                    coin = COIN(self.cell_width, self.cell_height)
                    #ensures the coins position is centered with thee x and y position in the cell that they spawn in
                    coin.pos = pygame.math.Vector2(centered_x, centered_y)
                    #updates the coins rect to be displayed on screen
                    coin.update_rect()
                    #adds coin to coin list
                    self.coin.append(coin)
                    #ends loop
                    break
                #adds an attempt if placement failed
                attempts +=1

        cutoff = 6 #Removes paths at the start of the game to ensure the user doesnt spawn near paths
        
        #Path config
        for row in range(total_cells):
            for col in range(total_cells):
                #Ensures the rows and collumns are in rows of 4 and collumns of 4
                if row % 2 == 0 and col % 2 == 0:
                    if row >= cutoff:
                        continue #ensures path element doesn't spawn near player
                    #calculates the x and y of the cells
                    x = col * self.cell_width
                    y = row * self.cell_height
                    path = PATHS(x, y, self.cell_width, self.cell_height)
                    #adds the paths via appending
                    self.paths.append(path) 
                    #tracks the top path
                if self.paths:
                    self.path_top_y = min(path.rect.y for path in self.paths)
                else:
                    self.path_top_y = SCREEN_HEIGHT
        
        #peds list for pedestrian placement
        self.peds = []
        #calculates the spawn row
        spawn_row = (SCREEN_HEIGHT - self.cell_height) // self.cell_height
        #ensure the peds spawn on the paths and cross gaps horizontally
        valid_rows = [row for row in range(total_cells) if row % 2 == 0 and row != spawn_row]
        
        #adds the amount of pedestrians that will spawn
        ped_rows = random.sample(valid_rows, 3)
        
        #for loop to establish the direction the pedestrians go and allows for left right movement
        for i, y_index in enumerate(ped_rows):
            y_pos = y_index * self.cell_height
            #This allows for the 2 different directions for the pedestrians
            directions = ["right", "left"][i % 2]
            ped = PEDS(SCREEN_WIDTH, y_pos, self.ped_group, 2, directions)
            #adds to pedestrian list
            self.peds.append(ped)

        #centers the player at the start            
        spawn_x = (SCREEN_WIDTH//2) - (self.cell_width//2)
        spawn_y = SCREEN_HEIGHT - self.cell_height
        self.player = CAR(spawn_x, spawn_y, 2)
    
    #allows positioning of player and for movement based on the position in the cell
    def move_player(self,dx,dy):
        move_x = self.cell_width
        move_y = self.cell_height
        
        #predicts player movement based on current position.
        pre_x = self.player.x + dx * move_x
        pre_y = self.player.y + dy * move_y
        
        #adds margins to ensure better collision with the player and path
        px_margin = 4
        
        #allows for slightly better collision but not pixel perfect.
        path_bound = pygame.Rect(pre_x + px_margin, pre_y + px_margin, self.player.rect.width - 2 * px_margin, self.player.rect.height - 2 * px_margin)
       
        
        #Allows for collisions to be updated when scrolling.
        for path in self.paths:
            if path.rect.y > SCREEN_HEIGHT:
                continue #if the path is off screen below
            #if the path rect and player rect hit it then prevents the player from going on the path.
            if path_bound.colliderect(path.rect):
                return 0
        
        #boundaries for left, right and bottom of the screen but not the top
        if pre_x < 0 or pre_x > SCREEN_WIDTH - self.player.rect.width:
            return 0
        if pre_y > SCREEN_HEIGHT - self.player.rect.height:
            return 0
        
        #if not hitting boundaries then move
        self.player.move_car(dx, dy, move_x, move_y)
        if dy == -1:
            self.score += 1

        #check if player has hit the top
        if self.player.y <= SCROLL_THRESH and self.scroll_targ == 0:
            self.scroll_targ = self.cell_height
        return self.scroll_speed
    
    #regenerate elements (important for scrolling)
    def regenerate(self):
        total_cells = (SCREEN_HEIGHT// self.cell_height)
        new_row_y = self.path_top_y - self.cell_height * total_cells

        for row in range(total_cells):
            for col in range(total_cells):
                #Ensures the rows and collumns are in rows of 4 and collumns of 4
                if row % 2 == 0 and col % 2 == 0:
                    x = col * self.cell_width
                    y = new_row_y + row * self.cell_height
                    path = PATHS(x, y, self.cell_width, self.cell_height)
                    #adds the paths via appending
                    self.paths.append(path) 
        
        #top of screen makes a new row of paths
        self.path_top_y = new_row_y
        self.world_row_Os += total_cells
        
        #coin spawning logic for the scrolling
        for _ in range(COIN_COUNT):
             #retry loop to avoid overlapping of coins
             attempts =  0
             while attempts < 100:
                #randomly places coins in a grid 
                col = random.randrange(1, self.total_cells_x, 2)
                row = random.randrange(1, total_cells, 2)
                
                #if the user reached the top of the screen this will create a new coins
                t_row = row + self.world_row_Os
                if(col, t_row) not in self.used_positions:
                    self.used_positions.add((col, t_row))
                    #calcuate position
                    x = col * self.cell_width
                    y = new_row_y + row * self.cell_height
                    #centers coins in road
                    centered_x = x + (self.cell_width - TILE_SIZE) // 2
                    centered_y = y + (self.cell_height - TILE_SIZE) // 2
                    
                    #new coins
                    new_coin = COIN(self.cell_width, self.cell_height)
                    new_coin.pos= pygame.math.Vector2(centered_x, centered_y)
                    new_coin.update_rect()
                    self.coin.append(new_coin)
                #end of loop
                    break
                attempts +=1
                self.regen_peds()
            
    #regenerates pedestrians
    def regen_peds(self):
        #calculates the spawn row
        total_cells = (SCREEN_HEIGHT// self.cell_height)
        spawn_row = (SCREEN_HEIGHT - self.cell_height) // self.cell_height
        #ensure the peds spawn on the paths and cross gaps horizontally
        valid_rows = [row for row in range(total_cells) if row % 2 == 0 and row != spawn_row]

        if len(valid_rows) < 3:
            return
        
        #adds the amount of pedestrians that will spawn
        ped_rows = random.sample(valid_rows, 3)
        
        #for loop to establish the direction the pedestrians go and allows for left right movement
        for i, y_index in enumerate(ped_rows):
            y_pos = self.path_top_y + y_index * self.cell_height
            #This allows for the 2 different directions for the pedestrians
            directions = ["right", "left"][i % 2]
            ped = PEDS(SCREEN_WIDTH, y_pos, self.ped_group, 2, directions)
            #adds to pedestrian list
            self.peds.append(ped)

    #update for scolling and the other game conditions that may change
    def update(self):
        #scrolling
        if self.scroll_targ > 0:
            scroll_step = min(self.scroll_speed, self.scroll_targ)
            self.scroll_targ -= scroll_step
            self.path_top_y += scroll_step
            
            #Generates new rows after threshold is crossed
            if self.path_top_y > -self.cell_height:
                self.regenerate()

           #allows elements to scroll
            for path in self.paths:
                path.rect.y += scroll_step
            for coin in self.coin:
                coin.rect.y += scroll_step
            for ped in self.peds:
                ped.rect.y += scroll_step
            self.player.y += scroll_step
            self.player.rect.y += scroll_step
            #removes elements after scrolling to prevent strain on resources
            self.paths = [p for p in self.paths if p.rect.y < SCREEN_HEIGHT + TILE_SIZE]
            self.coin = [c for c in self.coin if c.rect.y < SCREEN_HEIGHT + TILE_SIZE]
            self.peds = [ped for ped in self.peds if ped.rect.y < SCREEN_HEIGHT + TILE_SIZE]
        
        #ensures elements continue to spawn continuously on scrolling
        max_vis_row = (self.world_row_Os * self.cell_height) + SCREEN_HEIGHT + TILE_SIZE
        self.used_positions ={
            (col,row) for (col,row) in self.used_positions
            if row * self.cell_height < max_vis_row}
       
        #allows for pedestrians to be updated for their movement  
        for ped in self.peds:
            ped.update()
        self.check_collisions()

        #game over caused by colliding with the pedestrian
        for ped in self.peds:
            if ped.rect.colliderect(self.player.rect):
                self.hit_sound.play()
                if self.score > self.hi_score:
                    self.hi_score = self.score
                return self.game_over()

#Draws the elements
    def draw_elements(self):
        for path in self.paths:
            path.draw_path()
        for coin in self.coin:
            coin.draw_coin()
        for ped in self.peds:
            ped.draw()
        self.draw_Score()
   
    #Collisions  
    def check_collisions(self):
            for coin in self.coin:
            #coin collision
                if self.player.rect.colliderect(coin.rect):
                    #plays sound when coin is collected
                    self.coin_sound.play()
                    #Increases score by 10 points if coin is collected
                    self.score += 10
                    coin.randomize()
                    break
            
    #draws any text elements
    def draw_text(self, text, font, text_col, x, y, center = False):
        img = font.render(text, True, text_col)
        rect = img.get_rect()
        if center:
            rect.center =(x,y)
        else:
            rect.topleft = (x,y)
        screen.blit(img, rect)

    #score display   
    def draw_Score(self):
        score_text = (f"Score  {self.score}")
        score_surface = self.score_font.render(score_text, True ,(255,255,255))
        screen.blit(score_surface, (20,20)) 
    
    #displays high score on game over screen
    def draw_hi_score(self):
        hi_scoreText = (f"Hi-Score {self.hi_score}")
        score_surface = self.score_font.render(hi_scoreText, True,(255,255,255))
        screen.blit(score_surface, (20,20))

    #displays game over text options to quit or restart (ESC to quit, ENTER to restart)
    def game_over(self):
            gameOverMenu = True
            while gameOverMenu:
                screen.fill((0,0,0))
                pygame.draw.rect(screen, (255, 255, 255), (42, 60, 710, 520), width = 20)
                self.draw_text("Game Over!", self.game_font, (255,255,255), 70, 150)
                self.draw_text("Press ENTER to play again!", self.ui_font, (255,255,255), 250, 400)
                self.draw_text("Press ESC to Quit to main menu.", self.ui_font, (255,255,255), 250, 440)
                self.draw_hi_score()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            gameOverMenu = False
                            return MAIN()
                        elif event.key == pygame.K_ESCAPE:
                            gameOverMenu = False
                            return "menu"
                pygame.display.flip()   
#calls the main class to run the game.
def run():
    main_game = MAIN()
    clock = pygame.time.Clock()

    while True:
        #initial scroll variable to allow for scrolling
        scroll = 0
        for event in pygame.event.get():
            #allows user to close window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #movement for up, left and right arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    main_game.move_player(-1,0)
                elif event.key == pygame.K_RIGHT:
                        main_game.move_player(1,0)
                elif event.key == pygame.K_UP:
                        scroll = main_game.move_player(0,-1)
        
        #draw
        #colour of background
        screen.fill((56,56,56))

        #threshold invisible line for scrolling
        pygame.draw.line(screen, ((56,56,56)),(0,SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))
        
        #allows for the game to restart after a game over
        result = main_game.update()
        if isinstance(result, MAIN):
            main_game = result
        elif result == "menu":
            return "menu"

        #draws elements
        main_game.draw_elements()
        main_game.player.draw_car(screen)
    #update
        pygame.display.flip()
        #frame rate
        clock.tick(120)

#only runs the main game if the start button on the menu is clicked.
if __name__ == "__main__":
    run()           
  

        
        
         
