import pygame
import sys
import time
#importing my files (seperate to make the code more readable)
from FileHandling import HighScoresFunc
from Classes import Player, Monster
pygame.init()

#assiging and key variables, creating window...
WIDTH, HEIGHT = 600,400
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Dungeon Slayer")
FPS = 60
clock = pygame.time.Clock()

#colours...
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (218,0,0)

#options...
player_vel = 3
monster_vel = 1
show_hitboxes = False

#font sizes..
Bigfont = pygame.font.Font(None, 50)
Midfont = pygame.font.Font(None, 30)

#border used for highscore procedure...
BORDER = pygame.Rect((WIDTH//4, HEIGHT//16), (WIDTH//2, 7*HEIGHT//8))


#Loading in and scaling sprites.
CHAR_WIDTH, CHAR_HEIGHT = 50,50

player_pic1 = pygame.image.load("Sprites/player.png")
player_pic2 = pygame.image.load("Sprites/playerAnimation1.png")
player_atk = pygame.image.load("Sprites/player_attacking.png")
sword_atk = pygame.image.load("Sprites/sword_attacking.png")

monster_pic1 = pygame.image.load("Sprites/redOgre.png")
monster_pic2 = pygame.image.load("Sprites/redOgre2.png")

GameBackground = pygame.image.load("Sprites/Grass2.png")
GameBackground = pygame.transform.scale(GameBackground, (WIDTH, HEIGHT))

Health0 = pygame.image.load("Sprites/hearts0.png")
Health1 = pygame.image.load("Sprites/hearts1.png")
Health2 = pygame.image.load("Sprites/hearts2.png")
Health3 = pygame.image.load("Sprites/hearts3.png")
HeartsList = [Health0, Health1, Health2, Health3]

ScoreBox = pygame.image.load("Sprites/scoreBox.png")
ScoreBox = pygame.transform.scale(ScoreBox, (150, 33))

gameOverImage = pygame.image.load("Sprites/GameOver1.png")
gameOverImage = pygame.transform.scale(gameOverImage, (WIDTH, HEIGHT))

Background = pygame.image.load("Sprites/background.png")
Background = pygame.transform.scale(Background, (WIDTH,HEIGHT))

TitleScreen = pygame.image.load("Sprites/titlescreen1.png")
TitleScreen = pygame.transform.scale(TitleScreen, (WIDTH, HEIGHT))
MenuBlank = pygame.image.load("Sprites/MenuBlank.png")
MenuBlank = pygame.transform.scale(MenuBlank, (WIDTH, HEIGHT))

PauseMenu = pygame.image.load("Sprites/PauseMenu.png")
PauseMenu = pygame.transform.scale(PauseMenu, (WIDTH, HEIGHT))

#sound effect and music...
BackgroundMusic = pygame.mixer.music.load("Sounds/Music.mp3")
pygame.mixer.music.set_volume(0.2)

GameOverSnd = pygame.mixer.Sound("Sounds/GameOver.wav")




# procedures and main subroutine
def DisplayTitle():

    WIN.blit(TitleScreen, (0,0))
    
    run = True
    while run:
        clock.tick(FPS)

        pygame.display.update()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

def DisplayMenu():
    
    #Create 1 Player text and black rect
    p1txt = Bigfont.render("1 Player", 1, RED)
    p1txtRec = pygame.Rect(WIDTH//16, 3*HEIGHT//8, p1txt.get_width()+20, p1txt.get_height()+10)
    
    #Create 2 Player text and black rect
    p2txt = Bigfont.render("2 Player", 1, RED)
    p2txtRec = pygame.Rect(WIDTH//16, 5*HEIGHT//8, p2txt.get_width()+20, p2txt.get_height()+10)
    
    #Create Options text and black rect
    optionstxt = Bigfont.render("Options", 1, RED)
    optionstxtRec = pygame.Rect(WIDTH//16, 7*HEIGHT//8, optionstxt.get_width()+20, optionstxt.get_height()+10)

    #Create Controls text
    Controls1 = Midfont.render("WSAD to move, F to attack", 1, BLACK, WHITE)
    Controls2 = Midfont.render("Arrow keys to move, Rshift to attack", 1, BLACK, WHITE)
    
    
    
    run = True
    while run:
        clock.tick(FPS)
        WIN.blit(MenuBlank, (0,0))

        #draw 1 player text and rect
        pygame.draw.rect(WIN, BLACK, p1txtRec)
        WIN.blit(p1txt, (p1txtRec.x+10, p1txtRec.y+5))

        #draw 2 player text and rect
        pygame.draw.rect(WIN, BLACK, p2txtRec)
        WIN.blit(p2txt, (p2txtRec.x+10, p2txtRec.y+5))

        #draw options text and rect
        pygame.draw.rect(WIN, BLACK, optionstxtRec)
        WIN.blit(optionstxt, (optionstxtRec.x+10, optionstxtRec.y+5))

        #draw player 1's controls text
        WIN.blit(Controls1, (WIDTH//3, p1txtRec.y + p1txtRec.height//4))

        #draw player 2's controls text
        WIN.blit(Controls2, (WIDTH//3, p2txtRec.y + p2txtRec.height//4))
        

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if p1txtRec.collidepoint(event.pos):
                    print("1 Player Chosen")
                    return
                elif p2txtRec.collidepoint(event.pos):
                    print("2 Player hasnt been added yet...")
                elif optionstxtRec.collidepoint(event.pos):
                    print("Options has been chosen")
                    DisplayOptions()

def DisplayOptions():
    global player_vel, monster_vel, show_hitboxes
    

    run = True
    while run:

        clock.tick(FPS)

        WIN.blit(MenuBlank, (0,0))

        
        #PLAYER vel txt
        p_vel_txt = Midfont.render("Player Speed: " + str(player_vel), 1, BLACK, WHITE)
        WIN.blit(p_vel_txt, (WIDTH//16, 2*HEIGHT//6))
        #Increase Text and Rectangle
        p_vel_increase = Midfont.render("Increase", 1, RED, WHITE)
        p_inc_rect = pygame.Rect((WIDTH//2, 2*HEIGHT//6), (p_vel_increase.get_width(), p_vel_increase.get_height()))
        WIN.blit(p_vel_increase, (p_inc_rect.x, p_inc_rect.y))
        #Decrease Text and Rectangle
        p_vel_decrease = Midfont.render("Decrease", 1, RED, WHITE)
        p_dec_rect = pygame.Rect((WIDTH//2 + p_inc_rect.w + 2, 2*HEIGHT//6), (p_vel_increase.get_width(), p_vel_increase.get_height()))
        WIN.blit(p_vel_decrease, (p_dec_rect.x, p_dec_rect.y))


        #MONSTER vel txt
        m_vel_txt = Midfont.render("Monster Speed: " + str(monster_vel), 1, BLACK, WHITE)
        WIN.blit(m_vel_txt, (WIDTH//16, 3*HEIGHT//6))
        #Increase Text and Rectangle
        m_vel_increase = Midfont.render("Increase", 1, RED, WHITE)
        m_inc_rect = pygame.Rect((WIDTH//2, 3*HEIGHT//6), (m_vel_increase.get_width(), m_vel_increase.get_height()))
        WIN.blit(m_vel_increase, (m_inc_rect.x, m_inc_rect.y))
        #Decrease Text and Rectangle
        m_vel_decrease = Midfont.render("Decrease", 1, RED, WHITE)
        m_dec_rect = pygame.Rect((WIDTH//2 + m_inc_rect.w + 2, 3*HEIGHT//6), (m_vel_increase.get_width(), m_vel_increase.get_height()))
        WIN.blit(m_vel_decrease, (m_dec_rect.x, m_dec_rect.y))

        #HITBOXES
        Hitbox_txt = Midfont.render("Show hitbox: " + str(show_hitboxes), 1, BLACK, WHITE)
        WIN.blit(Hitbox_txt, (WIDTH//16, 4*HEIGHT//6))
        #switch text and rectangle
        hb_switch = Midfont.render("Show/Hide Hitbox", 1, RED, WHITE)
        hb_switch_rect = pygame.Rect((WIDTH//2, 4*HEIGHT//6), (hb_switch.get_width(), hb_switch.get_height()))
        WIN.blit(hb_switch, (hb_switch_rect.x, hb_switch_rect.y))

        #DEFAULT VALUES
        default = Midfont.render("DEFAULT VALUES", 1, WHITE, BLACK)
        default_rect = pygame.Rect((WIDTH//16, 5*HEIGHT//6), (default.get_width(), default.get_height()))
        WIN.blit(default, (default_rect.x, default_rect.y))

        #BACK TO MENU
        back_to_menu = Midfont.render("BACK TO MENU", 1, WHITE, BLACK)
        back_rect = pygame.Rect((WIDTH//2, 5*HEIGHT//6), (back_to_menu.get_width(), back_to_menu.get_height()))
        WIN.blit(back_to_menu, (back_rect.x, back_rect.y))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if p_inc_rect.collidepoint(event.pos) and player_vel < 10:
                    print("Player speed increased")
                    player_vel += 1
                if p_dec_rect.collidepoint(event.pos) and player_vel > 1:
                    print("Player speed decreased")
                    player_vel -= 1

                if m_inc_rect.collidepoint(event.pos) and monster_vel < 10:
                    print("monster speed increased")
                    monster_vel += 1
                if m_dec_rect.collidepoint(event.pos) and monster_vel > 1:
                    print("monster speed decreased")
                    monster_vel -= 1

                if hb_switch_rect.collidepoint(event.pos):
                    print("hitbox switched")
                    show_hitboxes = not show_hitboxes

                if default_rect.collidepoint(event.pos):
                    print("values set to default")
                    player_vel = 3
                    monster_vel = 1
                    show_hitboxes = False

                if back_rect.collidepoint(event.pos):
                    return

        
        pygame.display.update()
    

def GameOver():
    
    WIN.blit(gameOverImage, (0,0))
    pygame.display.update()

    GameOverSnd.play()
    time.sleep(1.5)

    run = True # checking for button clicks
    while run:
            
        clock.tick(FPS)
        
        pygame.display.update()
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False


def posx_middle(surface):
    return (WIDTH // 2) - (surface.get_width() // 2)

def AskName(score):

    enter_noti = Midfont.render("Type to enter your name...", 1, WHITE, BLACK)
    length_noti = Midfont.render("Name must not be greater than 10 characters", 1, WHITE, BLACK)
    score_text = Bigfont.render("You Scored: "+ str(score) ,1, WHITE)
    
    user_name = ""
    user_text = ""
    Complete = False
    correct_length = True
    
    run =  True
    while run:
        clock.tick(FPS)
        
        WIN.blit(Background, (0,0))
        pygame.draw.rect(WIN, BLACK, BORDER)
        pygame.draw.rect(WIN, WHITE, BORDER, 5)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    user_name = user_text
                    Complete = True
                    
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                    correct_length = True
                    
                else:
                    if len(user_text) < 10:
                        user_text += event.unicode
                    else:
                        correct_length = False



        name_text = Midfont.render(user_text, 1, BLACK, WHITE)
        
        WIN.blit(score_text, (posx_middle(score_text), HEIGHT//8))
        WIN.blit(enter_noti, (posx_middle(enter_noti), HEIGHT//3))
        WIN.blit(name_text, (posx_middle(name_text), HEIGHT//2))
        
        if not correct_length:
            WIN.blit(length_noti, (posx_middle(length_noti), 3*HEIGHT//4))
        
        pygame.display.update()

        if Complete:
            return user_name


def DisplayHighScores(HSList):
    
    # saving highscore in file etc

    #displaying lederboard + background
    WIN.fill(BLACK)
    WIN.blit(Background, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    pygame.draw.rect(WIN, WHITE, BORDER, 5)
    count = 0
    increase = BORDER.h // 12 - 1

    for item in HSList: # displaying name and score in right place 

        name = Midfont.render((str(item[0])), 1, WHITE)
        WIN.blit(name, (BORDER.x + 10, BORDER.y + count + 10))
    
        score = Midfont.render((str(item[1])), 1, WHITE)
        WIN.blit(score, (BORDER.x + BORDER.w - score.get_width() -20, BORDER.y + count + 10))
    
        count += increase

    pygame.display.update()
    
    run = True
    while run: # checking for button clicks

        pygame.display.update()

        clock.tick(FPS)
            

        for event in pygame.event.get(): #loops through and checks for events (QUIT)
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

                
                


def StartPause():
    
    run = True
    while run:
        clock.tick(FPS)
        WIN.blit(PauseMenu, (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return

    
def drawWindow(player1, monster1, monster2, monster3, Score):
    #filling Window and updating the display
    #WIN.fill(WHITE)
    WIN.blit(GameBackground, (0,0))
    
    player1.updateDisplay(WIN)
    monster1.updateDisplay(WIN)
    monster2.updateDisplay(WIN)
    monster3.updateDisplay(WIN)

    
    #collision box
    if show_hitboxes:
        pygame.draw.rect(WIN, (0,150,0), player1.obj, 1)
        pygame.draw.rect(WIN, (0,150,0), monster1.obj, 1)
        pygame.draw.rect(WIN, (0,150,0), monster2.obj, 1)
        pygame.draw.rect(WIN, (0,150,0), monster3.obj, 1)
        pygame.draw.rect(WIN, (0,150,0), player1.sword, 1)

    WIN.blit(ScoreBox, (100,0))
    WIN.blit(Score, (250,-1))

    
    pygame.display.update()


def main():

    pygame.mixer.music.play(-1)
    
    restart = True
    while restart:

        DisplayTitle()
        DisplayMenu()
        
        TotalScore = 0
    
        #create "player1" object from Player class. uses methods from class
        player1 = Player(CHAR_WIDTH, CHAR_HEIGHT, 200, 200, player_vel, 1)
        player1.CreateSprites(player_pic1, player_pic2, player_atk, sword_atk, HeartsList)
    
        #Monster1
        monster1 = Monster(CHAR_WIDTH, CHAR_HEIGHT, 600, 200, monster_vel)
        monster1.CreateSprites(monster_pic1, monster_pic2)
    
        #Monster2
        monster2 = Monster(CHAR_WIDTH, CHAR_HEIGHT, 0, 0, monster_vel)
        monster2.CreateSprites(monster_pic1, monster_pic2)
    
        #Monster3
        monster3 = Monster(CHAR_WIDTH, CHAR_HEIGHT, 300, 0, monster_vel)
        monster3.CreateSprites(monster_pic1, monster_pic2)
    
        
     
        ani_frame_count = 0
        do_animations = True
        
        run_game = True
        while run_game:
            
            clock.tick(FPS) #ticks 60 times a second (FPS)
            
            ani_frame_count += 1
            if ani_frame_count == 5:
                do_animations = True
                ani_frame_count = 0
            else:
                do_animations = False
            
            player1.checkAttack = True
            
            for event in pygame.event.get(): #loops through and checks for events (QUIT)
                if event.type == pygame.QUIT: 
                    run_game = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        StartPause()
                    
                    
    
                player1.checkForAttackPress(event)
                    
            #Player
            keysPressed = pygame.key.get_pressed() #gets pressed keys
            
            player1.movement(keysPressed)
            player1.animation(do_animations)
            player1.checkCollision(monster1)
            player1.checkCollision(monster2)
            player1.checkCollision(monster3)
            run_game = player1.PlayerHealth()
    
            #Monster1, 2, and 3
            monster1.movementTowardsPlayer1(player1)
            monster2.movementTowardsPlayer1(player1)
            monster3.movementTowardsPlayer1(player1)
            if do_animations:
                monster1.monsterAnimation()
                monster2.monsterAnimation()
                monster3.monsterAnimation()
            TotalScore += monster1.checkSwordCollision(player1)
            TotalScore += monster2.checkSwordCollision(player1)
            TotalScore += monster3.checkSwordCollision(player1)
            
            
            SCORE_TEXT = Bigfont.render((str(TotalScore)), 1, BLACK, WHITE)
            drawWindow(player1, monster1, monster2, monster3, SCORE_TEXT)#calls procedure to update display
        
        
        
        #Game Over AND High Score
    
        GameOver()#game over screen
                 
        name = AskName(TotalScore)
        list_leaderboard = HighScoresFunc(TotalScore, name)
        DisplayHighScores(list_leaderboard)

    
    pygame.quit() #deactivates Pygame 

main()#calls the main procedure
