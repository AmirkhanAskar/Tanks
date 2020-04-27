import pygame
import random
from enum import Enum

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Tanks")
shoot = pygame.mixer.Sound('shoot.wav')

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def life_tank(n, x, y, s):
    f = pygame.font.SysFont('serif', 30)
    lifet2 = f.render(s + str(n), True, (12, 97, 23))
    screen.blit(lifet2, (x, y))


class Tank:

    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = x
        self.y = y
        self.health = 3
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self):
        tank_c = (self.x + int(self.width/2), self.y + int(self.width/2))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width/2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x +
                                                          self.width+int(self.width/2), self.y+int(self.width/2)), 4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x -
                                                          int(self.width/2), self.y+int(self.width/2)), 4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x +
                                                          int(self.width/2), self.y - int(self.width/2)), 4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x +
                                                          int(self.width/2), self.y + self.width+int(self.width/2)), 4)

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

        if self.x > 800:
            self.x = 0
        if self.x < 0:
            self.x = 800
        if self.y > 600:
            self.y = 0
        if self.y < 0:
            self.y = 600

        self.draw()

    def fire(self):
        shoot.play()
        if tank1.direction == Direction.LEFT:
            bullet = Bullet(tank1.x - 20, tank1.y + 20, -10, 0, self.color)
        if tank1.direction == Direction.RIGHT:
            bullet = Bullet(tank1.x + 60, tank1.y + 20, 10, 0, self.color)
        if tank1.direction == Direction.UP:
            bullet = Bullet(tank1.x + 20, tank1.y - 20, 0, -10, self.color)
        if tank1.direction == Direction.DOWN:
            bullet = Bullet(tank1.x + 20, tank1.y + 60, 0, 10, self.color)
        bullets.append(bullet)


class Bullet:
    def __init__(self, x, y, velx, vely, color):
        self.x = x
        self.y = y
        self.brad = 4
        self.velx = velx
        self.vely = vely
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.brad)

    def move(self):
        self.x += self.velx
        self.y += self.vely

        self.draw()

mainloop = True
tank1 = Tank(300, 300, 2, (44, 50, 163))
tank2 = Tank(100, 100, 2, (161, 40, 48), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
bullets = []

FPS = 60
clock = pygame.time.Clock()

while mainloop:
    mill = clock.tick(FPS)
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False

            if event.key in tank1.KEY.keys():
                tank1.change_direction(tank1.KEY[event.key])
            if event.key in tank2.KEY.keys():
                tank2.change_direction(tank2.KEY[event.key])

            if event.key == pygame.K_SPACE:
                tank1.fire()

            if event.key == pygame.K_RETURN:
                tank2.fire()

    life_tank(tank1.health, 15, 15, 'Player 1: ')
    life_tank(tank2.health, 15, 50, 'Player 2: ')

    for b in bullets:
        b.move()

        if b.x < 0 or b.x > 800 or b.y < 0 or b.y > 600:
            bullets.pop(0)

        if b.x in range(tank1.x, tank1.x + 40) and b.y in range(tank1.y, tank1.y + 40):
            bullets.pop(0)
            tank1.health -= 1
        if b.x in range(tank2.x, tank2.x + 40) and b.y in range(tank2.y, tank2.y + 40):
            bullets.pop(0)
            tank2.health -= 1
        

    if tank1.health == 0 or tank2.health == 0:
        mainloop = False
    
    tank1.move()
    tank2.move()

    pygame.display.flip()

pygame.quit()

# Stoped watching lecture about tanks in 49:30
