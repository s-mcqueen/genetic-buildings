import shapely
from shapely.geometry.polygon import LinearRing

from pygooglechart import XYLineChart
import webbrowser

from pymunk.vec2d import Vec2d
from pymunk.util import *

import random

class Building:
    ''' a building has a list of verticies that define it as well as
        other features.
            * a density? weight?
            * cost? (space taken up on the ground)
            * height?
    '''
    def __init__(self, verticies):
        self.verticies = verticies  # a list of verticies defining this building
        self.poly = [Vec2d(v) for v in verticies]
        self.triangles = triangulate(self.poly)
        self.convexes = convexise(self.triangles)

        self.weight = 0  # a random value? 
        self.cost = 0  # some function of space taken on ground
        self.height = 0  # height is a property of the polygon

    def get_verticies(self):
        return self.verticies

    def set_verticies(self, new_verticies):
        self.verticies = new_verticies
        # need to reset related aspects of the building
        self.poly = [Vec2d(v) for v in verticies]
        self.triangles = triangulate(self.poly)
        self.convexes = convexise(self.triangles)

    def get_triangles(self):
        return self.triangles

    def get_convexes(self):
        return self.convexes

    def fitness(self):
        # return the fitness of this particular building
        return 0


class Population:
    def __init__(self, size):
        self.size = size
        self.buildings = []


    def get_buildings(self):
        return self.buildings

    def get_size(self):
        return self.size

    def fill(self):


    def fittest(self):
        # calculate the best building
        return 0

# RANDOM BUILDING GENERATION


def random_building():
    num_vertices = random.randint(3, 10) # at least 3, or else is a line
    vert = generate_verticies(num_vertices)
    while not valid_building(vert):
        vert = generate_verticies(num_vertices)

    # we know we have a valid set of verticies
    b = Building(vert)
    return b

def generate_verticies(num_vertices):
    vert = []
    for n in range(num_vertices):
        vert.append((random.randint(0,15), random.randint(0,15))) # tuple represents a point
    return vert


def valid_building(v):
    ''' returns true if a polygon is simple (meaning none of its edges
        cross each other). our definition of a valid building is a simple polygon '''
    building = LinearRing(v) # shapely
    return building.is_simple # shapely




    # make it into a polygon
    # triangulate / convexise polygon (pymunk.utils)
        # put these polygons together -- this is our building


# POPULATION GENERATION

# for size_of_population:
    # RANDOM BUIDLING GENERATION

# FITNESS

# CROSSOVER

# MUTATION 

b = random_building()
print b.get_convexes()
