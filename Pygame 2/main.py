import pygame 
from sys import exit
from random import randint, choice
#First line we need in pygame.
#It starts pygame and initializes stuffs in it.
#It's like starting a car.

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,232))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)
    #Makes player jump. - code with same functionality exists in while loop.
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 232:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 232:
            self.rect.bottom = 232

    def animation_state(self):
        if self.rect.bottom < 232:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos  = 232

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= 100:
            self.kill()        


pygame.init()

def obstacle_movement(obstacle_list):

    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: 
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > - 100]
        return obstacle_list #Used to make code in function a global variable, instead of using the "global" key word.
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time
    
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 232:
        player_surf = player_jump
    else: 
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]



    #play walking anime if player is on floor.
    #display jump surface if player not on floor.

#Creating a display surface - the window the user will see.
screen = pygame.display.set_mode((800,400))
#Name of game window.
pygame.display.set_caption("Gamer")

#MAXIMUM FRAME RATE.
#Clock object to help with time and controlling the frame rate.
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
music = pygame.mixer.Sound("audio/music.wav")
music.play(loops = -1)

#GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

#Font
text_font = pygame.font.Font('font/Pixeltype.ttf', 30)
#Sky image.
sky_surface = pygame.image.load("graphics/hallo-sky.png").convert()
#Ground image.
ground_surface = pygame.image.load("graphics/ground.png").convert()
"""
score_surf = text_font.render("SCORE", False, (64, 64, 64))
score_rect = score_surf.get_rect(center = (40, 15))
"""

#Obstacles
#Snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]
snail_x = 600
snail_rect = snail_surface.get_rect(topleft = (snail_x,200))


#Fly
fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]


obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,230))
#GRAVITY
player_gravity = 0
#MENU
player_stand = pygame.image.load("graphics\Player\player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))
#MENU'S FONT
title_font = text_font.render("Grapple One", False, "green") #Font surface
title_rect = title_font.get_rect(midbottom = (400,100))
#Instruction
msg = text_font.render("Press SPACE to start", False, "green")
msg_rect = msg.get_rect(midtop=(400, 300))

#TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) #Triggers event in certain intervals.

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


#Keeps code running forever.
while True:
    for event in pygame.event.get():
        #Used to close the window. without it the windown will keep on running without closing.
        if event.type == pygame.QUIT:
            pygame.quit()
            #Most secure way to close pygame is to use the "sys module." "exit()" is imported from the sys module.
            exit()
        
        if game_active:
            #MOUSE POSITON.
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 232: 
                    player_gravity = -20
            
            #KEYBOARD INPUT CONTROLS USING EVENTS.
            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 232:
                    player_gravity = -20

            #TIMER FOR SNAIL.
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            #TIMER FOR FLY.
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index == 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800 
                start_time = int(pygame.time.get_ticks()/1000)


        if event.type == obstacle_timer:
            obstacle_group.add(Obstacle(choice(["fly","snail","snail","snail",])))
            """
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(topleft = (randint(900,1100),200)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(topleft = (randint(900,1100),110)))
            """
    if game_active:

        screen.blit(sky_surface,(0, 0))
        screen.blit(ground_surface, (0,232))
       
        score = display_score()        

        #Obstacle movement.
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        #Collisions
        game_active = collision_sprite()
        #game_active = collisions(player_rect, obstacle_rect_list)
        #SIMULATION GROUND COLLISION. 
        if player_rect.bottom >= 232:
            player_rect.bottom = 232

    
        #PLAYER
        """
        player_gravity += 1
        player_rect.y += player_gravity
        screen.blit(player_surf, player_rect )
        screen.blit(snail_surface, snail_rect)
        snail_rect.left -= 3
        if snail_rect.right <= 0: snail_rect.left = 800
        player_animation()
        """
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #COLLISION 
        if snail_rect.colliderect(player_rect):
            #pygame.quit()
            #exit() 
            game_active = False
    
    else:
        #EXITS TO MENU SCREEN IF GAME IS OVER.
        mnu = pygame.image.load("graphics/menu-screen.png")
        mnu = pygame.transform.scale(mnu, (800, 400))
        mnu_rect = mnu.get_rect()
        mnu_rect = mnu_rect.move((0, 0))

        screen.blit(mnu, mnu_rect)
        #screen.fill((94, 129, 162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,230)
        player_gravity = 0

        screen.blit(title_font, title_rect)
        screen.blit(msg, msg_rect)

        score_msg = text_font.render(f"Your score: {score}", False,"green")
        score_rect = score_msg.get_rect(center=(400,330))
        

        if score == 0: screen.blit(msg,msg_rect)
        else: screen.blit(score_msg,score_rect)
        
 
    #Draw all elements and update everything.
    pygame.display.update()
    #Calling the clock object to run 60fps.
    clock.tick(60)


#RESOURCE
"""
KEYBOARD INPUT CONTROLS USING "pygame.key"
key = pygame.key.get_pressed()
if key[pygame.K_SPACE]:
""" 
#COLLISION
#Using colliderect to chech for collision.
#if player_rect.colliderect(snail_rect):
#  print("collision")
"""
mouse_coor = pygame.mouse.get_pos()
if player_rect.collidepoint(mouse_coor):
print(pygame.mouse.get_pressed())  
"""

# pygame.draw.rect(screen, "#c0e8ec", score_rect)
       # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        #pygame.draw.ellipse(screen,"Brown", pygame.Rect(50,200,100,100))
       # screen.blit(score_surf, score_rect)

#screen.blit(player_surf(80, 200))
        #snail_x -= 4
        #snail_rect.left -= 4 #Updated version - using rect instead of image surface.
        #Snail movement restrictions.
        #if snail_x < 0:
            #snail_x = 800 