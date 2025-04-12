# importing required package
import random
import sys
import pygame
import time
from pygame.locals import *

# Game Settings
Fps = 32
Screen_width = 289  
Screen_height = 511  
Screen = pygame.display.set_mode((Screen_width, Screen_height))
Ground_y = Screen_height * 0.75  # Y-position of the ground (base)

# File paths for game assets
Player = "GameSprites\\bird.png"
Background = "GameSprites\\background.png"
Game_pipe = "GameSprites\\pipe.png"

# We are going to load all the images and sounds in it.
Game_images = {}
GameSounds = {}
icon = pygame.image.load("GameSprites\\pranitlogo.png")
pygame.display.set_icon(icon)


def welcomescreen():
    """This is a welcome screen that displays as game starts 
    """
    playerx = int(Screen_width / 2.5) + 17
    playery = int((Screen_height - Game_images["player"].get_height()) / 2.5)
    messagex = int((Screen_width - Game_images["message"].get_width()) / 2 + 5)
    messagey = int(Screen_height * 0.08)
    messagex2 = messagex + 88
    messagey2 = messagey + 35
    basex = 0

    # Loop runs until the player starts or exits the game
    while True:
        for i in pygame.event.get():
            if i.type == QUIT or (i.type == KEYDOWN and i.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif i.type == KEYDOWN and (i.key == K_SPACE or i.key == K_UP):
                return
            else:
                Screen.blit(Game_images["background"],
                            (0, 0))  # if want use this to increase asspect ratio ---> 409,730
                Screen.blit(Game_images["player"], (playerx, playery))
                Screen.blit(Game_images["message"], (messagex, messagey))
                Screen.blit(Game_images["message2"], (messagex2, messagey2))
                Screen.blit(Game_images["ready"], (messagex + 45, messagey2 + 80))
                Screen.blit(Game_images["base"],
                            (basex, Ground_y))  # pygame.transform.scale(Game_images["base"],(410,300)
                pygame.display.update()
                Fpsclock.tick(Fps)


def maingame():
    """ this is main game logic that runs after welcome screen if user
        presses the space bar or up key"""
    score = 0
    playerx = int(Screen_width / 5)
    playery = int(Screen_height / 2)
    basex = 0
    pipe1 = randompipes()
    pipe2 = randompipes()

    upperpipe = [
        {'x': Screen_width + 200, 'y': pipe1[0]['y']},
        {'x': Screen_width + 200 + (Screen_width / 2), 'y': pipe2[0]['y']}
    ]
    lowerpipe = [
        {'x': Screen_width + 200, 'y': pipe1[1]['y']},
        {'x': Screen_width + 200 + (Screen_width / 2), 'y': pipe2[1]['y']}
    ]
    pipevelX = -4 # pipe moving speed to left
    playervelY = -10  # Initial upward velocity when flapped
    playermaxvelY = 10  # Max downward velocity
    playerAccvelY = 1  #This is like a force that gradually increases the bird's downward speed
    playerflapaccv = -8  # player flapped velocity
    playerflapped = False

    # Game loop
    while True:
        for i in pygame.event.get():
            if i.type == QUIT or (i.type == KEYDOWN and i.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if i.type == KEYDOWN and (i.key == K_SPACE or i.key == K_UP):
                if playery > 0:
                    playervelY = playerflapaccv  # from -10 to -8
                    playerflapped = True
                    GameSounds["wing"].play()
            
        # Check for collisions
        crashtest = isCollide(playerx, playery, upperpipe, lowerpipe)
        if crashtest:
            Game_over(score)
            return

        playermidpos = playerx + Game_images['player'].get_width() / 2

        # Score update when player crosses pipe
        for pipe in upperpipe:
            pipemidpos = pipe['x'] + Game_images['pipe'][0].get_width() / 2
            if pipemidpos <= playermidpos < pipemidpos + 4:
                score += 1
                GameSounds['point'].play()
                

         # Apply gravity
        if playervelY < playermaxvelY and not playerflapped:
            playervelY += playerAccvelY
        if playerflapped:
            playerflapped = False
        
        # Apply vertical velocity to player position, but prevent falling below ground
        playerheight = Game_images['player'].get_height()
        playery = playery + min(playervelY,Ground_y - playerheight - playery)   # this will not let the bird go inside the ground

        # Move pipes to the left
        for uppipe, lowpipe in zip(upperpipe, lowerpipe):
            uppipe['x'] += pipevelX
            lowpipe['x'] += pipevelX

        # Add new pipes
        if 0 < upperpipe[0]['x'] < 5:
            newpipe = randompipes()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])

        # Remove pipes that go off screen
        if upperpipe[0]['x'] < -Game_images['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)
        
        # Bliting game sprites on screen
        Screen.blit(Game_images["background"], (0, 0))
        for uppipe, lowpipe in zip(upperpipe, lowerpipe):
            Screen.blit(Game_images["pipe"][0], (uppipe['x'], uppipe['y']))
            Screen.blit(Game_images["pipe"][1], (lowpipe['x'], lowpipe['y']))
        Screen.blit(Game_images["base"], (basex, Ground_y))
        Screen.blit(Game_images["player"], (playerx, playery))

         # Display score
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += Game_images['numbers'][digit].get_width()

        Xoffset = (Screen_width - width) / 2
        for digit in mydigits:
            Screen.blit(Game_images["numbers"][digit], (Xoffset, Screen_height * 0.12))
            Xoffset += Game_images["numbers"][digit].get_width()
        pygame.display.update()
        Fpsclock.tick(Fps)
        


def isCollide(playerx, playery, uppipe, lowpipe):
    """it checks is the player collide with pipe or ground or get outside the screen
    """
    # Check if bird hits ground or goes above screen
    if playery > Ground_y - 42 or playery < 0:
        GameSounds['hit'].play()
        return True
    
    # Collision with upper pipes
    for pipe in uppipe:
        pipHeight = Game_images['pipe'][0].get_height()
        if playery < pipHeight + pipe['y'] and abs(playerx - pipe['x']) < Game_images['pipe'][0].get_width():
            GameSounds['hit'].play()
            return True

    # Collision with lower pipes
    for pipe in lowpipe:
        if (playery + Game_images['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < Game_images['pipe'][0].get_width():
            GameSounds['hit'].play()
            return True

    return False


def randompipes():
    """This function will generate random pipes"""

    pipeheight = Game_images["pipe"][0].get_height()
    pipes_gap = Screen_height / 3.2
    y2 = pipes_gap + random.randrange(0, int(Screen_height - Game_images["base"].get_height() - 1.2 * pipes_gap))
    pipex = Screen_width + 10
    y1 = pipeheight - y2 + pipes_gap
    pipe = [
        {'x': pipex, 'y': -y1}, # upper pipe
        {'x': pipex, 'y': y2} # lower pipe
    ]
    return pipe


def Game_over(score):
    """ Displays the Game Over screen."""

    pygame.time.delay(350)  # Small delay to let the hit sound play
    GameSounds['die'].play()
    # coordinate for gameover message
    messagex_cord = int((Screen_width - Game_images["gameover"].get_width()) / 2)
    messagey_cord = int(Screen_height * 0.2)

    # Game screen after game over
    Screen.blit(Game_images["background"], (0, 0))
    Screen.blit(Game_images["base"], (0, Ground_y))
    Screen.blit(Game_images["gameover"], (messagex_cord, messagey_cord))
    Screen.blit(Game_images['score'], (messagex_cord + 45, messagey_cord + 75))

    # final score
    mydigits = [int(x) for x in str(score)]
    width = sum(Game_images['numbers'][digit].get_width() for digit in mydigits)
    num_width = (Screen_width - width) / 2

    for digit in mydigits:
        Screen.blit(Game_images["numbers"][digit], (num_width, Screen_height * 0.4))
        num_width += Game_images["numbers"][digit].get_width()

    # updating the screen
    pygame.display.update()
    Fpsclock.tick(Fps)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

# Main execution starts here
if __name__ == '__main__':
    pygame.init()
    Fpsclock = pygame.time.Clock()
    pygame.display.set_caption("FlappyBird_PranitBijave")

    # Load all game assets
    Game_images['numbers'] = (
        pygame.image.load("GameSprites\\0.png").convert_alpha(),
        pygame.image.load("GameSprites\\1.png").convert_alpha(),
        pygame.image.load("GameSprites\\2.png").convert_alpha(),
        pygame.image.load("GameSprites\\3.png").convert_alpha(),
        pygame.image.load("GameSprites\\4.png").convert_alpha(),
        pygame.image.load("GameSprites\\5.png").convert_alpha(),
        pygame.image.load("GameSprites\\6.png").convert_alpha(),
        pygame.image.load("GameSprites\\7.png").convert_alpha(),
        pygame.image.load("GameSprites\\8.png").convert_alpha(),
        pygame.image.load("GameSprites\\9.png").convert_alpha()
    )
    Game_images["message"] = pygame.image.load("GameSprites\\logo.png").convert_alpha()
    Game_images["message2"] = pygame.image.load("GameSprites\\logo2.png").convert_alpha()
    Game_images["base"] = pygame.image.load("GameSprites\\base.png").convert_alpha()
    Game_images["ready"] = pygame.image.load("GameSprites\\ready.png")
    Game_images["pipe"] = (
        pygame.transform.rotate(pygame.image.load(Game_pipe).convert_alpha(), 180),
        pygame.image.load(Game_pipe).convert_alpha()
    )
    Game_images["background"] = pygame.image.load(Background).convert()
    Game_images["player"] = pygame.image.load(Player).convert_alpha()
    Game_images["gameover"] = pygame.image.load("GameSprites\\gameover.png").convert_alpha()
    Game_images["score"] = pygame.image.load("GameSprites\\score.png").convert_alpha()

    GameSounds["die"] = pygame.mixer.Sound("GameSounds\\die.mp3")
    GameSounds["hit"] = pygame.mixer.Sound("GameSounds\\hit.mp3")
    GameSounds["wing"] = pygame.mixer.Sound("GameSounds\\wing.mp3")
    GameSounds["swoosh"] = pygame.mixer.Sound("GameSounds\\swoosh.mp3")
    GameSounds["point"] = pygame.mixer.Sound("GameSounds\\point.mp3")
    
    # Game loop: keeps repeating welcome and game
    while True:
        welcomescreen()
        maingame()
