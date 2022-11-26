import pygame
from button import Button
from pygame import mixer
from fighter import Fighter
#from pyvidplayer import Video


mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game-Project")
BG = pygame.image.load("assets/night.png").convert_alpha()
BG1 = pygame.image.load("assets/treess.jpg").convert_alpha()
icon1 = pygame.image.load('assets/images/Characters/Shaheen/wind_hashashin.png').convert_alpha()
icon2 = pygame.image.load("assets/images/Characters/Priestess/water_priestess.png").convert_alpha()
#vid = Video('assets/intro/gamemade.mp4')

#vid.set_size((1280,720))



    

def get_font(size):  
    return pygame.font.Font("assets/font.ttf", size)

def maingame() :


    #set framerate
    clock = pygame.time.Clock()
    FPS = 60

    #define colours
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    #define game variables
    intro_count = 4
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]#player scores. [P1, P2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    #define fighter variables
    SHAHEEN_SIZE_WIDTH = 288
    SHAHEEN_SIZE_HEIGHT = 128
    SHAHEEN_SCALE = 4
    SHAHEEN_OFFSET = [135, 85]
    SHAHEEN_DATA = [SHAHEEN_SIZE_WIDTH,SHAHEEN_SIZE_HEIGHT, SHAHEEN_SCALE, SHAHEEN_OFFSET]
    
    PRIESTESS_SIZE_WIDTH = 288
    PRIESTESS_SIZE_HEIGHT = 128
    PRIESTESS_SCALE = 4
    PRIESTESS_OFFSET = [135, 85]
    PRIESTESS_DATA = [PRIESTESS_SIZE_WIDTH,PRIESTESS_SIZE_HEIGHT, PRIESTESS_SCALE, PRIESTESS_OFFSET]

    #WARRIOR_SIZE_WIDTH = 288
    #WARRIOR_SIZE_HEIGHT = 128
   # WARRIOR_SCALE = 4
   # WARRIOR_OFFSET = [135, 85]
    #WARRIOR_DATA = [WARRIOR_SIZE_WIDTH,WARRIOR_SIZE_HEIGHT, WARRIOR_SCALE, WARRIOR_OFFSET]



    #load music and sounds
    pygame.mixer.music.load("assets/audio/battlemusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)
    sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    sword_fx.set_volume(0.5)
    magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
    magic_fx.set_volume(0.75)

    #load background image
    bg_image = pygame.image.load("assets/images/background/plainforest.webp").convert_alpha()

    #load spritesheets
    shaheen_sheet = pygame.image.load("assets/images/Characters/Shaheen/Shaheen_sprites_288x128.png").convert_alpha()
    priestess_sheet = pygame.image.load("assets/images/Characters/Priestess/Priestess_sprites_288x128.png").convert_alpha()

    #load vicory image
    victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

    #define number of steps in each animation
    SHAHEEN_ANIMATION_STEPS = [8 , 8 , 3 , 3 , 7 , 6 , 8 , 18 , 26 , 30 , 8 , 6 , 19]
    PRIESTESS_ANIMATION_STEPS = [8 , 10 , 8 , 3 , 3 , 8 , 6 , 7 , 21 , 27 , 32 , 12 , 12 , 7 , 16]
    WARRIOR_ANIMATION_STEPS = [8 , 8 , 3 , 3 , 20 , 8 , 8 , 11 , 19 , 28 ,18 , 10 , 6, 13 ]   


    #define font
    count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

    #function for drawing text
    def draw_text(text, font, text_col, x, y):
      img = font.render(text, True, text_col)
      screen.blit(img, (x, y))

    #function for drawing background
    def draw_bg():
      scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
      screen.blit(scaled_bg, (0, 0))
    def draw_icon():
      screen.blit(icon1, (70,0))
      screen.blit(icon2, (630,0))

    #function for drawing fighter health bars
    def draw_health_bar(health, x, y):
      ratio = health / 100
      pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
      pygame.draw.rect(screen, RED, (x, y, 400, 30))
      pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


    #create two instances of fighters
    fighter_1 = Fighter(1, 360, 430, False, SHAHEEN_DATA, shaheen_sheet, SHAHEEN_ANIMATION_STEPS, sword_fx)
    fighter_2 = Fighter(2, 860, 430, True, PRIESTESS_DATA, priestess_sheet, PRIESTESS_ANIMATION_STEPS, magic_fx)

    #game loop


    run = True
    while run:

      clock.tick(FPS)

      #draw background
      draw_bg()

      #show player stats
      draw_health_bar(fighter_1.health, 140, 20)
      draw_health_bar(fighter_2.health, 690, 20)
      draw_text("shaheen: " + str(score[0]), score_font, 'yellow', 140, 60)
      draw_text("lyna: " + str(score[1]), score_font, 'yellow', 690, 60)
      draw_icon()

      #update countdown
      if intro_count <= 0:
        #move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
      else:
        #display count timer
        draw_text(str(intro_count), count_font, 'yellow', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
          intro_count -= 1
          last_count_update = pygame.time.get_ticks()

      #update fighters
      fighter_1.update_p1()
      fighter_2.update_p2()

      #draw fighters
      fighter_1.draw(screen)
      fighter_2.draw(screen)

      #check for player defeat
      if round_over == False:
        if fighter_1.alive == False:
          score[1] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
          score[0] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
      else:
        #display victory image
        screen.blit(victory_img, (480, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
          round_over = False
          intro_count = 3
          fighter_1 = Fighter(1, 360, 430, False, SHAHEEN_DATA, shaheen_sheet, SHAHEEN_ANIMATION_STEPS, sword_fx)
          fighter_2 = Fighter(2, 860, 430, True, PRIESTESS_DATA, priestess_sheet, PRIESTESS_ANIMATION_STEPS, magic_fx)

      #event handler
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()


      #update display
      pygame.display.update()

def options():
    pygame.mixer.music.load("assets/audio/medival.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        new_bg2 = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(new_bg2, (0, 0))

        OPTIONS_TEXT = get_font(25).render("'w-a-d' or 'Up-Left-Right' to move.", True, "yellow")
        OPTIONS_RECT1 = OPTIONS_TEXT.get_rect(center=(540, 100))
        OPTIONS_atk = get_font(25).render("'r-t' or '1-2' to attack.", True, "yellow")
        OPTIONS_RECT2 = OPTIONS_TEXT.get_rect(center=(540, 150))
        OPTIONS_spatk = get_font(25).render("'y' or '3' for special attack while below 40 hp.", True, "yellow")
        OPTIONS_RECT3 = OPTIONS_TEXT.get_rect(center=(540, 200))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT1)
        screen.blit(OPTIONS_atk, OPTIONS_RECT2)
        screen.blit(OPTIONS_spatk, OPTIONS_RECT3)
        OPTIONS_BACK = Button(image=None, pos=(640, 660), 
                            text_input="BACK", font=get_font(75), base_color="yellow", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    pygame.mixer.music.load("assets/audio/fantasy.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)


    while True:


        new_bg2 = pygame.transform.scale(BG1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(new_bg2, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="#90ee90")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="#90ee90")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="#90ee90")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    maingame()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    

        pygame.display.update()

#def intro():

    pygame.mixer.music.load("assets/audio/heavymetal.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)
    clock = pygame.time.Clock()
    videolengh = 460
    vid = Video('assets/intro/Kraken.mp4')
    vid.set_size((1280,720))
    while True:
        
        
        vid.draw(screen, (0, 0))
        pygame.display.update()
        videolengh -= 1
        clock.tick(100)
        if videolengh <= 0 :
          vid.close()
          main_menu()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                main_menu()


main_menu()
#exit pygame


pygame.quit()