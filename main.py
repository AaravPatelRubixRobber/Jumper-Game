import pygame
import time
import random


pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Roboto', 30)

#makes colors
black = (0,0,0)
white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (0, 155, 0)
dark_green = (0, 200, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
yellow = (255, 255, 0)
grey = (100, 100, 100)

screen_x, screen_y = 900, 600
screen = pygame.display.set_mode((screen_x, screen_y), 0, 32)

clock = pygame.time.Clock()

#the class for the player(a square)
class player:
    def __init__(self, pos):
        self.color = blue
        self.x = pos[0]
        self.y = pos[1]
        self.side_len = 50

        #helps for update movement
        self.jumping = False
        self.rate_of_change = 0

        self.deaths = 0
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.side_len, self.side_len))

    def update_pos(self):#does movement for player
        pressed = pygame.key.get_pressed()
        
        #for gravity
        self.y = int(self.y - self.rate_of_change)
            
        if pressed[pygame.K_LEFT]:
            self.x  -= 2
            
        if pressed[pygame.K_RIGHT]:
            self.x  += 2
            
        if pressed[pygame.K_UP] and self.jumping == False:
            #jumps
            self.rate_of_change += 5
            self.jumping = True
        else:
            self.rate_of_change -= .1

        #prevents the player from going off the screen
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.side_len > screen_x:
            self.x = screen_x - self.side_len
        

    def reset(self, start_pos):
        #resets the player
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.deaths += 1

    def full_reset(self):
        #full resets the player
        self.deaths = 0
        self.x = 0
        self.y = 1000
            
            
        

#the class for a triangle that hurts the human on impact
class spike:
    def __init__(self, pos, side_len):
        self.x = pos[0]
        self.y = pos[1]
        self.color = red
        self.side_len = side_len

    def draw(self):
        #draws a spike
        pygame.draw.polygon(screen, self.color, ((self.x,self.y),(self.x - self.side_len//2, self.y + self.side_len),(self.x + self.side_len//2, self.y + self.side_len)))


#just a normal floor
class floor:
    def __init__(self, pos, width):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.color = black

    def draw(self):
        #draws a floor
        pygame.draw.line(screen, self.color, (self.x, self.y+3), (self.x + self.width, self.y+3), 6)

#a floot that can move
class moving_floor(floor):
    
    def __init__(self, pos, width, end_pos, move_speed):

        super().__init__(pos, width)

        self.start_x = pos[0]
        self.start_y = pos[1]
        
        self.end_x = end_pos[0]
        self.end_y = end_pos[1]
        if self.end_x > self.x:
            self.change_x = move_speed
        else:
            self.change_x = -move_speed

        if self.end_y > self.y:
            self.change_y = move_speed
        else:
            self.change_y = -move_speed
            
        
    def update_pos(self):
        #updates the floor's pos

        if (self.change_x > 0 and self.x + self.change_x > max(self.end_x, self.start_x)) or (self.change_x < 0 and self.x + self.change_x < min(self.end_x, self.start_x)):
            self.change_x *= -1
        else:
            self.x += self.change_x
            
        if (self.change_y > 0 and self.y + self.change_y > max(self.end_y, self.start_y)) or (self.change_y < 0 and self.y + self.change_y < min(self.end_y, self.start_y)):
            self.change_y *= -1
        else:
            self.y += self.change_y

#makes a floor of acid
class acid(floor):
    def __init__(self, pos, width):
        super().__init__(pos, width)
        self.y -= 2
        self.color = green
    def draw(self):
        #draws the acid
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.width, self.y), 3)

#makes the portal to get to the next level
class portal:
    def __init__(self, pos, side_len):
        self.x = pos[0]
        self.y = pos[1]
        self.side_len = side_len
        self.color = purple
    def draw(self):
        #draws the portal
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.side_len, self.side_len))

#makes a level with all the widgets I made earlier    
class level:
    def __init__(self, start_pos, portal, spikes = [], floors =[], moving_floors = [], acids = []):
        self.spikes = spikes
        self.floors = floors
        self.acids = acids
        self.moving_floors = moving_floors
        self.start_pos = start_pos
        self.portal = portal

#makes the home screen(the first screen the user encounters)
class home_screen:
    def __init__(self, btn_pos, btn_side_len):
        self.btn_x = btn_pos[0]
        self.btn_y = btn_pos[1]
        self.btn_side_len = btn_side_len
        self.btn_color = purple
        self.bg_color = white
    def draw(self):
        #draws the home screen
        screen.fill(self.bg_color)
        
        myfont = pygame.font.SysFont('Roboto', 100)
        textsurface = myfont.render("Jumper", False, green)
        text_rect = textsurface.get_rect(center=(screen_x//2, screen_y//2 - 200))
        screen.blit(textsurface,text_rect)
                    
        pygame.draw.rect(screen, self.btn_color, (self.btn_x, self.btn_y, self.btn_side_len, self.btn_side_len))
        pygame.draw.polygon(screen, black, ((self.btn_x + 2*self.btn_side_len//3, self.btn_y + self.btn_side_len//2), (self.btn_x + self.btn_side_len//3, self.btn_y + self.btn_side_len//3), (self.btn_x + self.btn_side_len//3, self.btn_y + 2*self.btn_side_len//3)))
    def PRESS_PLAY(self):

        #check if the player pressed play
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.btn_x < mouse_x < self.btn_x + self.btn_side_len and self.btn_y < mouse_y < self.btn_y + self.btn_side_len:
                return True
        return False

#makes the level select screen
class level_select:
    def __init__(self, levels, levels_per_row, side_len):
        self.levels_per_row = levels_per_row
        self.side_len = side_len
        self.color = blue
        self.txt_color = purple
    def draw(self):

        #draws the level select screen
        screen.fill(white)

        myfont = pygame.font.SysFont('Roboto', 150)
        textsurface = myfont.render("Level Select", False, self.txt_color)
        text_rect = textsurface.get_rect(center=(screen_x//2, screen_y//2 - 200))
        screen.blit(textsurface,text_rect)

        #makes a grid of levels for the user to select
        for level_num in range(len(levels)):

            level = levels[level_num]
            col_num = level_num % self.levels_per_row
            row_num = level_num // self.levels_per_row

            alloted_x = screen_x
            alloted_y = screen_y - 200

            x = int((alloted_x/self.levels_per_row)*(col_num + 0.5) - self.side_len/2)
            y = int((alloted_y/(len(levels)/self.levels_per_row))*(row_num + 0.5) - self.side_len/2) + 200
            
            pygame.draw.rect(screen, self.color, (x, y, self.side_len, self.side_len))

            myfont = pygame.font.SysFont('Roboto', 40)
            textsurface = myfont.render(str(level_num + 1), False, self.txt_color)
            text_rect = textsurface.get_rect(center=(x + self.side_len//2, y + self.side_len//2))
            screen.blit(textsurface,text_rect)

    def PRESS_LEVEL(self): #returns a list of whether the level is pressed and which level is pressed

        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for level_num in range(len(levels)):

            level = levels[level_num]
            col_num = level_num % self.levels_per_row
            row_num = level_num // self.levels_per_row

            alloted_x = screen_x
            alloted_y = screen_y - 200

            x = int((alloted_x/self.levels_per_row)*(col_num + 0.5) - self.side_len/2)
            y = int((alloted_y/(len(levels)/self.levels_per_row))*(row_num + 0.5) - self.side_len/2) + 200
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if x < mouse_x < x + self.side_len and y < mouse_y < y + self.side_len:
                    return [True, level_num]

        return [False, -1]


        
    
        
#integrates all of the levels, home screen, and gives most of the logic for the program
class game:
    def __init__(self, player, levels):
        self.bg_color = white
        self.player = player
        self.levels = levels
        self.current_level_num = 0
        self.current_level = self.levels[self.current_level_num]

        self.exit_game = False
        self.start_time = pygame.time.get_ticks()
        self.current_time =(pygame.time.get_ticks()-self.start_time)/1000

    def draw(self):
        #draws the level
        screen.fill(white)

        self.current_level.portal.draw()

        for spike in self.current_level.spikes:
            spike.draw()

        for floor in self.current_level.floors:
            floor.draw()

        for moving_floor in self.current_level.moving_floors:
            moving_floor.draw()

        for acid in self.current_level.acids:
            acid.draw()

        self.player.draw()

        #shows deaths
        textsurface = myfont.render("Deaths: " + str(self.player.deaths), False, black)
        screen.blit(textsurface,(0,0))

        #shows level
        textsurface = myfont.render("Level: " + str(self.current_level_num + 1), False, black)
        screen.blit(textsurface,(0,20))

        #shows time
        textsurface = myfont.render("Time: " + str(self.current_time), False, black)
        screen.blit(textsurface,(0,40))

        

    def PLAYER_HIT_FLOOR(self):
        #check if the player hit a floor
        for floor in self.current_level.floors:
            if self.player.y < floor.y < self.player.y + self.player.side_len and floor.x - self.player.side_len < self.player.x <floor.x + floor.width:#checks if the player hit the floor
                if self.player.rate_of_change < 0:#makes it so the player doesnt double jump from floors

                    #fixes up the location of the player so he doesn't become wedged between the floors
                    self.player.y = floor.y - self.player.side_len
                    
                    return True

        for floor in self.current_level.moving_floors:
            if self.player.y < floor.y < self.player.y + self.player.side_len and floor.x - self.player.side_len < self.player.x <floor.x + floor.width:#checks if the player hit the floor
                if self.player.rate_of_change < 0:#makes it so the player doesnt double jump from floors

                    #fixes up the location of the player so he doesn't become wedged between the floors
                    self.player.y = floor.y - self.player.side_len
                    
                    return True
                
        return False

    def PLAYER_HIT_SPIKE(self):
        #checks if a player hit a spike
        for spike in self.current_level.spikes:
            if spike.x - spike.side_len//2 - self.player.side_len + 2*(spike.y-(self.player.y)) < self.player.x < spike.x + spike.side_len//2 - 2*(spike.y-(self.player.y)):
                if spike.y - spike.side_len//2 - self.player.side_len < self.player.y < spike.y + spike.side_len//2:
                    return True
        return False

    def PLAYER_HIT_ACID(self):
        #checks if a player fell into the acid
        for floor in self.current_level.acids:
            if self.player.y < floor.y < self.player.y + self.player.side_len and floor.x - self.player.side_len < self.player.x <floor.x + floor.width:#checks if the player hit the floor
                return True
        return False

    def PLAYER_FELL_OFF(self):
        #checks if a player fell of the map
        return self.player.y + self.player.side_len > screen_y

    def PLAYER_HIT_PORTAL(self):
        #checks if the player hit a portal
        p = self.current_level.portal
        if p.x  - self.player.side_len< self.player.x < p.x + p.side_len:
            if p.y  - self.player.side_len< self.player.y < p.y + p.side_len:
                return True
        return False

    def start_timer(self):
        #starts the timer
        self.start_time = pygame.time.get_ticks()
        self.current_time = ((pygame.time.get_ticks()-self.start_time)/1000)

    def reset(self):
        #resets a level
        self.player.reset(self.current_level.start_pos)

    def full_reset(self):
        #resets the game
        self.current_level = levels[0]
        self.current_level_num = 0
        
        self.player.full_reset()

    def go_to_level(self, num):
        #goes to a certain level
        self.current_level_num = num
        self.current_level = levels[num]
        self.player.x = self.current_level.start_pos[0]
        self.player.y = self.current_level.start_pos[1]
        

    def update_pos(self):

        #updates the time
        self.current_time =(pygame.time.get_ticks()-self.start_time)/1000

        #updates all pos
        self.player.update_pos()
        for moving_floor in self.current_level.moving_floors:
            moving_floor.update_pos()
        
        if self.PLAYER_HIT_FLOOR():
            self.player.rate_of_change = 0
            self.player.jumping = False
        if self.PLAYER_HIT_SPIKE():
            self.reset()
            
        if self.PLAYER_HIT_ACID():
            self.reset()
            
        if self.PLAYER_FELL_OFF():
            self.reset()
            
        if self.PLAYER_HIT_PORTAL():
            try:
                #goes to the next level
                self.current_level_num += 1
                self.current_level = levels[self.current_level_num]
                self.player.deaths -= 1
                self.reset()

                
            except:
                #makes end screen

                self.exit_game = True
                
                if True:

                    self.player.rate_of_change = 0
                    
                    myfont = pygame.font.SysFont('Roboto', 100)
                    textsurface = myfont.render("You Won!", False, black)
                    text_rect = textsurface.get_rect(center=(screen_x//2, screen_y//2 - 200))
                    screen.blit(textsurface,text_rect)

                    myfont = pygame.font.SysFont('Roboto', 50)
                    textsurface = myfont.render("Press Space To Return Home", False, black)
                    text_rect = textsurface.get_rect(center=(screen_x//2, screen_y//2 + 100))
                    screen.blit(textsurface,text_rect)

                    pressed = pygame.key.get_pressed()
                    pygame.display.update()

                    go = True
                    while go:
                        
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                 pygame.quit()
                                 exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE: # replace the 'p' to whatever key you wanted to be pressed
                                    self.full_reset()
                                    pygame.display.update()
                                    go = False
                                    break
                            
                                 
                        
                        
                """while True:
                    if pressed[pygame.K_w]:
                        print("hi")
                        self.full_reset()
                        pygame.display.update()
                        break"""
                    
                    
                    

                

    
        
#creates objects for everything
p = player([100, 450])

l_1 = level([50, 0],
            portal([700, 450], 50),
            floors = [floor([50, 500], 500)],
            moving_floors = [moving_floor([200, 400], 100, [400, 400], 2)],
            acids = [acid([250, 500], 100)])

l_2 = level([0, 450],
            portal([700, 25], 50),
            spikes = [spike([300, 250], 50), spike([400, 450], 50)],
            floors = [floor([0, 500], 600), floor([650, 400], 100), floor([200, 300], 600), floor([100, 200], 100), floor([300, 100], 500)])

l_3 = level([0, 50],
            portal([800, 425], 50),
            spikes = [spike([450, 250], 50)],
            floors = [floor([0, 100], 100), floor([150, 200], 100), floor([300, 300], 300), floor([650, 400], 100), floor([800, 500], 100)])

l_4 = level([0, 450],
            portal([800, 25], 50),
            spikes = [spike([450, 250], 50), spike([650, 150], 50)],
            floors = [floor([0, 500], 100), floor([150, 400], 100), floor([300, 300], 200), floor([550, 200], 200), floor([800, 100], 100)])

l_5 = level([0, 450],
            portal([800, 25], 50),
            acids = [acid([400, 200], 100)],
            spikes = [spike([150, 450], 50)],
            floors = [floor([0, 500], 200), floor([200, 400], 100), floor([100, 300], 100), floor([300, 200], 300)],
            moving_floors = [moving_floor([650, 100], 100, [850, 100], 2)])

l_6 = level([0, 0],
            portal([800, 25], 50),
            acids = [acid([400, 550], 100)],
            spikes = [spike([325, 200], 50),spike([625, 500], 50), spike([125, 350], 50)],
            floors = [floor([0, 100], 250), floor([250, 250], 100), floor([100, 400], 150), floor([200, 550], 600)],
            moving_floors = [moving_floor([600, 400], 100, [800, 400], 2), moving_floor([500, 300], 50, [700, 300], 3), moving_floor([600, 200], 100, [800, 200], 2)])

levels = [l_1, l_2, l_3, l_4, l_5, l_6]

home = home_screen([screen_x//2 - 75, screen_y//2 - 75], 150)
choose_level = level_select(levels, 3, 125)

g = game(p, levels)

run = True

state = "home"

#main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if state == "home":
        home.draw()
        if home.PRESS_PLAY():
            state = "level_select"

    if state == "level_select":
        choose_level.draw()
        pressed, level_num = choose_level.PRESS_LEVEL()
        if pressed:
            g.go_to_level(level_num)
            g.start_timer()
            state = "game"

    if state == "game":
        g.draw()
        g.update_pos()
        if g.exit_game:
            state = "level_select"
            g.exit_game = False

    clock.tick(150)
    pygame.display.update()

