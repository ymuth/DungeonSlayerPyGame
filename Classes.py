import pygame
import random
pygame.init()

#adding dound effects
HurtSnd = pygame.mixer.Sound("Sounds/Hurt.wav")
HurtSnd.set_volume(1)
SlashSnd = pygame.mixer.Sound("Sounds/Slash.wav")
SlashSnd.set_volume(0.3)
PointGained = pygame.mixer.Sound("Sounds/pointScore.wav")
PointGained.set_volume(0.1)

WIDTH, HEIGHT = 600,400

class Humanoid:

    def __init__(self, width, height, posx, posy, vel):
        # constructor
        
        self.obj = pygame.Rect((posx, posy), (width, height)) # creating a rectangle for object
        
        self.VEL = vel
        self.direction = 1
        self.total_steps = 0 #direction of player and steps moved for movement()

    def CreateSprites(self, aniRight1, aniRight2):
        # procedure which creates a list of right and left sprites scaled
        # using the width and height assigned in the constructor.
        self.rightPic1 = pygame.transform.scale(aniRight1, (self.obj.width,self.obj.height))
        self.rightPic2 = pygame.transform.scale(aniRight2, (self.obj.width,self.obj.height))
        self.RightAni = [self.rightPic1, self.rightPic2]

        self.leftPic1 = pygame.transform.flip(self.rightPic1, True, False)
        self.leftPic2 = pygame.transform.flip(self.rightPic2, True, False)
        self.LeftAni = [self.leftPic1, self.leftPic2] 
        
        self.SPRITE = self.RightAni[0] #sprite used or animation/image

    def updateDisplay(self, Window):
        Window.blit(self.SPRITE, (self.obj.x, self.obj.y))







class Player(Humanoid):

    keys1 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN,pygame.K_UP, pygame.K_RSHIFT]
    keys2 = [pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w, pygame.K_f]
    
    def __init__(self, width, height, posx, posy, vel, key_choice): # constructor
        
        super().__init__(width, height, posx, posy, vel) # INHERITS everythign from Humanoid constructor
        
        self.sword = pygame.Rect((posx, posy), (width, height)) # creating a rectangle for sword object
        self.attack_pressed = False 
        self.checkAttack = True
        self.HP = 3
        
        if key_choice == 0:
            self.key_choice = self.keys1
        else:
            self.key_choice = self.keys2 #choice of keys (wsad or arrow keys)


        #CreateSprites() Method is INEHRITED from Humanoid super class
    

    def CreateSprites(self, aniRight1, aniRight2, AniPlayerAtk, AniSwordAtk, Hearts):

        super().CreateSprites(aniRight1, aniRight2) #INHERITS FROM HUMANOID (adds player sprites)

        #adds sword sprites

        self.rightAtk = pygame.transform.scale(AniPlayerAtk, (self.obj.width,self.obj.height))
        self.leftAtk = pygame.transform.flip(self.rightAtk ,True, False)
        self.AttackAni = [self.leftAtk, self.rightAtk]

        self.rightSwd = pygame.transform.scale(AniSwordAtk, (self.obj.width,self.obj.height))
        self.leftSwd = pygame.transform.flip(self.rightSwd ,True, False)
        self.SwdAni = [self.leftSwd, self.rightSwd]

        self.SWORD_SPRITE = self.SwdAni[1]

        #adds Health sprites

        self.Hearts = Hearts
        self.HEART_SPRITE = self.Hearts[3]
        
        

    def movement(self, keysPressed): #movement
        self.previous_steps = self.total_steps # creating an attrivute called previous steps.
        temp_steps = self.previous_steps
        
        if keysPressed[self.key_choice[0]] and self.obj.x > 0: # LEFT
            self.obj.x -= self.VEL
            temp_steps = self.total_steps + 1
            self.direction = 0
        if keysPressed[self.key_choice[1]] and self.obj.x + self.obj.w < WIDTH: # RIGHT
            self.obj.x += self.VEL
            temp_steps = self.total_steps + 1
            self.direction = 1
        if keysPressed[self.key_choice[2]] and self.obj.y + self.obj.h < HEIGHT: # DOWN
            self.obj.y += self.VEL
            temp_steps = self.total_steps + 1
        if keysPressed[self.key_choice[3]] and self.obj.y > 0: # UP
            self.obj.y -= self.VEL
            temp_steps = self.total_steps + 1


        self.sword.y = self.obj.y
        if self.attack_pressed:
            if self.direction == 0:
                self.sword.x = self.obj.x - self.obj.width
            else:
                self.sword.x = self.obj.x + self.obj.width
        else:
            self.sword.x = WIDTH + 100 # out of screen
        
        
            
        self.total_steps = temp_steps 
        # self.total_steps will increase by only one even if
        # many keys are pressed at the same time.
        

    def animation(self, do_animation):
        sprite_choice = self.total_steps % 2 #number switches between 0 and 1 
        
        if self.attack_pressed:
            self.SPRITE = self.AttackAni[self.direction] # Atk aniamtion in current direction
            self.SWORD_SPRITE = self.SwdAni[self.direction]
        elif do_animation:
            if self.total_steps > self.previous_steps: #if movement has occured since last pass/frame
                if self.direction == 0:
                    self.SPRITE = self.LeftAni[sprite_choice]
                else:
                    self.SPRITE = self.RightAni[sprite_choice]
            else:
                if self.direction == 0:
                    self.SPRITE = self.LeftAni[0]
                else:
                    self.SPRITE = self.RightAni[0]

    def updateDisplay(self, Window):

        super().updateDisplay(Window) #INHERTIS from HUMANOID
        
        Window.blit(self.SWORD_SPRITE, (self.sword.x, self.sword.y))
        Window.blit(self.HEART_SPRITE, (0,0))


    def checkForAttackPress(self, event):
        if event.type == pygame.KEYDOWN and self.checkAttack:
            if event.key == self.key_choice[4]:
                SlashSnd.play()
                self.attack_pressed = True
                self.checkAttack = False
            else:
                self.attack_pressed = False
        elif self.checkAttack:
                self.attack_pressed = False


    def checkCollision(self, enemy):
        if self.obj.colliderect(enemy.obj):
            HurtSnd.play()
            self.HP -= 1
            if enemy.direction == 0:
                enemy.obj.x += 50
            elif enemy.direction == 1:
                enemy.obj.x -= 50


    def PlayerHealth(self):
        if self.HP > 0 and self.HP <= 3:
            self.HEART_SPRITE = self.Hearts[self.HP]
        if self.HP <= 0:
            return False
        else:
            return True






class Monster(Humanoid):

    #__init__() Constructor method is fully inherited

    #CreateSprites() method is also here from the Humanoid super class

    #updateDisplay() is INHERITED from humanoid class

    def movementTowardsPlayer1(self, player1):
        self.total_steps += 1
        
        if player1.obj.x > self.obj.x:
            self.obj.x += self.VEL
            self.direction = 1
        elif player1.obj.x < self.obj.x:
            self.obj.x -= self.VEL
            self.direction = 0

        if player1.obj.y > self.obj.y:
            self.obj.y += self.VEL
        elif player1.obj.y < self.obj.y:
            self.obj.y -= self.VEL

    

    def monsterAnimation(self):
        sprite_choice = self.total_steps % 2
        
        if self.direction == 0:
            self.SPRITE = self.LeftAni[sprite_choice]
        else:
            self.SPRITE = self.RightAni[sprite_choice]

    def checkSwordCollision(self, player):
        if self.obj.colliderect(player.sword):
            PointGained.play()
            self.death()
            return 1
        else:
            return 0

    def death(self):
        sideChoice = random.randint(0,1)
        if sideChoice == 0:
            self.obj.x = random.choice([0, WIDTH])
            self.obj.y = random.randint(0, HEIGHT)
        else:
            self.obj.x = random.randint(0, WIDTH)
            self.obj.y = random.choice([0, HEIGHT])
