import shapely
from shapely.geometry.polygon import LinearRing
from shapely.geometry.polygon import Polygon

from pygooglechart import XYLineChart
import webbrowser

from pymunk.vec2d import Vec2d
from pymunk.util import *

import random


global i

class Polypoly:
    """ a polygon has a list of verticies that define it 
    """
    def __init__(self, verticies, target):
        
        self.verticies = verticies  # a list of verticies defining this polygon
        self.target = target # target does not exist at first

        self.poly = [Vec2d(v) for v in verticies] # a pymunk polygon reprsentation
        self.triangles = triangulate(self.poly)
        self.convexes = convexise(self.triangles) # convexes representing the shape

    def get_verticies(self):
        return self.verticies

    def set_verticies(self, new_verticies):
        self.verticies = new_verticies
        # need to reset related aspects of the polygon
        self.poly = [Vec2d(v) for v in verticies]
        self.triangles = triangulate(self.poly)
        self.convexes = convexise(self.triangles)

    def get_poly(self):
        return self.poly

    def get_triangles(self):
        return self.triangles

    def get_convexes(self):
        return self.convexes

    def fitness(self):
        """ return the fitness of this particular polygon
             - - want to minimize this value - -
        """
        a = Polygon(self.verticies)
        b = Polygon(self.target.get_verticies())

        difference = a.symmetric_difference(b)
        return difference.area

    def graph(self):
        """ graph the polygon using google charts
        """
        chart = XYLineChart(200, 200, x_range=(0, 200), y_range=(0, 200))

        xdata = []
        ydata = []

        for n in self.verticies:
            x,y = n
            xdata.append(x)
            ydata.append(y)
        chart.add_data(xdata)
        chart.add_data(ydata)
        webbrowser.open(chart.get_url())


class Population:
    def __init__(self, size, fill, target):
        self.size = size
        self.polygons = []
        self.target = target
        if fill:
            self.generate()

    def generate(self):
        for n in range(self.size):
            # construct a random polygon and add it to the population
            self.polygons.append(random_polygon(self.target))

    def get_polygons(self):
        return self.polygons

    def get_size(self):
        return self.size

    def fill(self):
        return 0

    def fittest(self):
        best = float('inf')
        best_so_far = 0
        for p in self.polygons:
            fit = p.fitness()
            if (best > fit):
                best = fit
                best_so_far = p
        return (best_so_far, best)

def generate_verticies(num_vertices):
    global i
    i += 1
    vert = []
    for n in range(num_vertices):
        vert.append((random.randint(20,200), random.randint(20,200))) # tuple represents a point
    return vert

def valid_poly(v):
    """ returns true if a set of vertices contructs a simple and counter-clockwise polygon
        
        simple = no edges cross each other
        counter-clockwise = in practice this seems important!
    """
    poly = LinearRing(v)
    return (poly.is_simple and poly.is_ccw)

def random_polygon(target):
    num_vertices = random.randint(3, 10) # at least 3, or else is a line
    vert = generate_verticies(num_vertices)
    while not valid_poly(vert):
        # verticies need to construct counter clockwise, simple polygons
        vert = generate_verticies(num_vertices)

    # we know we have a valid set of verticies
    b = Polypoly(vert, target)
    return b


def run_tournament():
    return 0


def valid_crossover(parent1, parent2):
    vert = crossover(parent1, parent2)
    while not valid_poly(vert):
        vert = crossover(parent1, parent2)

    # return the child
    return Polypoly(vert)


def vertex_not_in_list(v, lst):
    for l in lst:
        if (v == l):
            return False
    return True

def crossover(parent1, parent2):
    # parents are polypolys

    child_verts = []

    # choose one parent to select an initial path from
    if (random.randint(1,2) == 1):
        chosen = parent1.get_verticies()
        other = parent2.get_verticies()
    else:
        chosen = parent2.get_verticies()
        other = parent1.get_verticies()

    # get a random section of verticies from parent1    
    start_i = 1
    end_i = 0
    while (start_i >= end_i): 
        # while loop ensures no "backwards" sections
        v1 = random.choice(chosen)
        v2 = random.choice(chosen)
        start_i = chosen.index(v1)
        end_i = chosen.index(v2)

    # add these verticies
    child_verts = chosen[start_i:end_i]


    return child_verts



# fitness:
# how big the symmetric difference is between a given shape, and a target shape
# shapely built in function: object.symmetric_difference(other)

# most fit:
# lowest symmetric difference to the target shape

# crossover -- should have many children
# some section of verticies from parent1
# some other section of verticies from parent2

# mutation
# randomly add or take away a new vertex / slightly alter a current vertex 


def set_i_to_zero():
    global i 
    i = 0
    return



# # tester code 
set_i_to_zero()


# tar = random_polygon(None)
# tar.graph()

# p = Population(40, True, tar)
# print "made pop"
# (best, value) = p.fittest()
# best.graph()
# print value
# print "i" + str(i)