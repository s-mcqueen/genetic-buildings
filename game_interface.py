import building_evolution # our evolution interface

# game interface
import pygame
from pygame.locals import *

# physics
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.util import *
from pymunk.pygame_util import draw_space, from_pygame

import random # you never know

# variable declarations
FPS=60
TIME_STEP=1.0/FPS  # time step
SCREEN_WIDTH, SCREEN_HEIGHT=800, 800

# pygame set up
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('genetic buildings')
clock = pygame.time.Clock()

# pymunk set up
space = pymunk.Space()   
space.gravity = 0,-1000  # this seems high?

def place_building(building, coords):

    vects = building.get_convexes()  # its not this, but its not poly.. 

    for v in vects:

        b_body = pymunk.Body(pymunk.inf, pymunk.inf)
        b_body.position = coords
        b_shape = pymunk.Poly(b_body, v)
        b_shape.elasticity = 1.0
        b_shape.color = pygame.color.THECOLORS['blue']

        space.add(b_body, b_shape)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: 
                running = False
            elif event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                new_building = building_evolution.random_building()
                place_building(new_building, event.pos)


        # make our screen white
        screen.fill(pygame.color.THECOLORS["white"])
        
        # draw the space
        pymunk.pygame_util.draw_space(screen, space)

        # update physics
        space.step(TIME_STEP)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print "done"

if __name__ == '__main__':
    main()
