# import building_evolution # our evolution interface
import target_poly_evolution

# game interface
import pygame
from pygame.locals import *

# physics
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.util import *
from pymunk.pygame_util import draw_space, from_pygame


# variable declarations
FPS=60
TIME_STEP=1.0/FPS  # time step
SCREEN_WIDTH, SCREEN_HEIGHT=1400, 800

# pygame set up
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('genetic buildings')
clock = pygame.time.Clock()

# pymunk set up
space = pymunk.Space()   
space.gravity = 0,0  # this seems high?

def flipy((x,y)):   
    """ hack to convert chipmunk physics to pygame coordinates"""
    return (x, -y+SCREEN_HEIGHT)

def place_polygon(polygon, coords, color):

    vects = polygon.get_convexes()

    b_body = pymunk.Body(pymunk.inf, pymunk.inf)
    b_body.position = coords

    space.add(b_body)

    for v in vects:

        b_shape = pymunk.Poly(b_body, v, (0,0), True)

        b_shape.elasticity = 1.0
        b_shape.color = pygame.color.THECOLORS[color]

        space.add(b_shape)


def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT: 
                running = False
            elif event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                running = False
            elif event.type == MOUSEBUTTONDOWN:

                tar = target_poly_evolution.Polypoly(None, [])
                p = target_poly_evolution.Population(100, tar)

                for i in range(40):  # number of generations
                    p = target_poly_evolution.evolve(p, 20)

                (a,b) = p.fittest()

                place_polygon(tar, flipy(event.pos), 'black')
                place_polygon(a, flipy(event.pos), 'red')

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
