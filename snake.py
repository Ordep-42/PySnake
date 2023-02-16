import pygame
from pygame.locals import *
from random import randrange

pygame.init()
window = 600
screen = pygame.display.set_mode([window] * 2)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
#divide the play area into a grid
tileSize = 20
range = (tileSize // 2, window - tileSize // 2, tileSize)
getRandomPosition = lambda: [randrange(*range), randrange(*range)]
#create snake
snake = pygame.rect.Rect([0, 0, tileSize - 1, tileSize - 1])
snake.center = getRandomPosition()
snakeLength = 3
snakeSegments = [snake.copy()]
snakeDirection = (0, 0)
#create apple
apple = snake.copy()
apple.center = getRandomPosition()

def gameStart():
    global snakeLength, snakeDirection, snakeSegments
    snake.center, apple.center = getRandomPosition(), getRandomPosition() #resets snake and apple positions
    snakeLength, snakeDirection = 3, (0,0) #resets snakes size
    snakeSegments = [snake.copy()]

directions = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1} #dictionary for prohibiting backwards movement
    
while True:
    clock.tick(10)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #snake controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and directions[pygame.K_UP]:
                    snakeDirection = (0, -tileSize)
                    directions = {pygame.K_UP: 1, pygame.K_DOWN: 0, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
                if event.key == pygame.K_DOWN and directions[pygame.K_DOWN]:
                    snakeDirection = (0, tileSize)
                    directions = {pygame.K_UP: 0, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}
                if event.key == pygame.K_LEFT and directions[pygame.K_LEFT]:
                    snakeDirection = (-tileSize, 0)
                    directions = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 0}
                if event.key == pygame.K_RIGHT and directions[pygame.K_RIGHT]:
                    snakeDirection = (tileSize, 0)
                    directions = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 0, pygame.K_RIGHT: 1}
                    
    screen.fill((0, 0, 0)) #makes the background black
    #check for snake colliding with itself
    selfEating = pygame.Rect.collidelist(snake, snakeSegments[:-3]) != -1
    #restarts the game for self eating or out of bounds
    if snake.top < 0 or snake.bottom > window or snake.left < 0 or snake.right > window or selfEating:
        gameStart()

    #eating mechanic
    if snake.center == apple.center:
        apple.center = getRandomPosition() #respawns the apple
        snakeLength += 1 #increases snake size

    #draw objects in the screen
    [pygame.draw.rect(screen, 'green', segment) for segment in snakeSegments]
    pygame.draw.rect(screen, 'red', apple)

    #snake movement animation
    snake.move_ip(snakeDirection)
    snakeSegments.append(snake.copy())
    snakeSegments = snakeSegments[-snakeLength:]

    pygame.display.update()