# mostly just trash in this file -- some of it might 

import pygame
from pygame.locals import *

import Box2D
from Box2D.b2 import *
import random

from pygooglechart import XYLineChart
import webbrowser

PPM=20.0 # pixels per meter
FPS=60
T_STEP=1.0/FPS  # time step
SCREEN_WIDTH, SCREEN_HEIGHT=800, 800

# pybox2d set up
w = world(gravity=(0,0), doSleep=True)


def rand_building(world):
    angle = random.randint(0,360)
    angle = 0
    position = (20,20)
    num_vertices = random.randint(3, 7)
    v = []
    for n in range(num_vertices):
        v.append((random.randint(0,15), random.randint(0,15)))

    print num_vertices
    print v
    dynamic_body = world.CreateDynamicBody(position=position, angle=angle)
    building=dynamic_body.CreatePolygonFixture(
                        vertices=v,
                        density=2, 
                        friction=2
                        )

    # graph the building -- testing concavity

    chart = XYLineChart(200, 200, 
                        x_range=(0, 200), y_range=(0, 200))


    xdata = []
    ydata = []

    for n in v:
        x,y = n
        xdata.append(x*10)
        ydata.append(y*10)
    chart.add_data(xdata)
    chart.add_data(ydata)
    webbrowser.open(chart.get_url())

def rand_ground_building(world):
    # make sure 2 vertices are on the ground
    return 0



def new_game(world):

    COLORS = {
        staticBody  : (23,44,131,254),
        dynamicBody : (40,40,40,255),
    }

    # Pygame setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    #create the ground
    ground_body = world.CreateStaticBody(
        position = (0,1),
        shapes = polygonShape(box=(50,5)),
        )

    ## random building
    rand_building(world)
    ## 


    running = True
    while running:
        # check for quit conditions
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                running = False

        screen.fill((0,0,0,0))
        for body in world.bodies:
            for fixture in body.fixtures:
                shape = fixture.shape
                vertices=[(body.transform*v)*PPM for v in shape.vertices]

                # flip
                vertices=[(v[0], SCREEN_HEIGHT-v[1]) for v in vertices]
                pygame.draw.polygon(screen, COLORS[body.type], vertices)

        # velocity iterations, position iterations
        world.Step(T_STEP, 10, 10)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print "done"



new_game(w)



