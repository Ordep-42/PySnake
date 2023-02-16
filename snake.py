import pygame
from pygame.locals import *
from random import randrange

pygame.init()

window = 600
screen = pygame.display.set_mode([window] * 2)
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()
time, timeStep = 0, 90 #control variable and delay between snake steps in milliseconds (makes snake go faster or slower)
gamePause = False

#divide the play area into a grid
tileSize = 20
tileRange = (tileSize // 2, window - tileSize // 2, tileSize)
getRandomPosition = lambda: [randrange(*tileRange), randrange(*tileRange)]

#create snake
snake = pygame.rect.Rect([0, 0, tileSize - 1, tileSize - 1])
snake.center = getRandomPosition()
snakeLength = 3
snakeSegments = [snake.copy()]
snakeDirection = (0, 0)
directions = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1} #dictionary for prohibiting backwards movement

#create apple
apple = snake.copy()
apple.center = getRandomPosition()

def gameStart():
    global snakeLength, snakeDirection, snakeSegments, gameRunning, gamePause
    snake.center, apple.center = getRandomPosition(), getRandomPosition() #resets snake and apple positions
    snakeLength, snakeDirection = 3, (0,0) #resets snakes size
    snakeSegments = [snake.copy()]
    
def drawObjects():    #draw objects in the screen
    [pygame.draw.rect(screen, 'green', segment) for segment in snakeSegments]
    pygame.draw.rect(screen, 'red', apple)

while True:

    while gamePause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gamePause = False
                
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #snake controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamePause = True
                elif event.key == pygame.K_UP and directions[pygame.K_UP]:
                    snakeDirection = (0, -tileSize)
                    directions = {pygame.K_UP: 1, pygame.K_DOWN: 0, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
                elif event.key == pygame.K_DOWN and directions[pygame.K_DOWN]:
                    snakeDirection = (0, tileSize)
                    directions = {pygame.K_UP: 0, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
                elif event.key == pygame.K_LEFT and directions[pygame.K_LEFT]:
                    snakeDirection = (-tileSize, 0)
                    directions = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 0}
                elif event.key == pygame.K_RIGHT and directions[pygame.K_RIGHT]:
                    snakeDirection = (tileSize, 0)
                    directions = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 0, pygame.K_RIGHT: 1}
                    
    screen.fill((20, 20, 20)) #makes the background dark gray
    #check for snake colliding with itself
    selfEating = pygame.Rect.collidelist(snake, snakeSegments[:-3]) != -1
    if selfEating: gameStart() #restarts the game for self eating

    #if the snake goes out of bounds it reappears on the opposite side
    if snake.y > 601:
        snake.y = -19
    elif snake.y < -19:
        snake.y = 601
    elif snake.x > 601:
        snake.x = -19
    elif snake.x < -19:
        snake.x = 601

    #eating mechanic
    if snake.center == apple.center:
        apple.center = getRandomPosition() #respawns the apple
        snakeLength += 1 #increases snake size
    drawObjects()
    #creates a time interval according to the current game time
    timeNow = pygame.time.get_ticks()
    if timeNow - time > timeStep: #as soon as the time interval is greater then the time step the snake will move and the time will be updated
        time = timeNow
        #snake movement animation
        snake.move_ip(snakeDirection)
        snakeSegments.append(snake.copy())
        snakeSegments = snakeSegments[-snakeLength:]

    pygame.display.update()
    clock.tick(60)