import shapely
from shapely.geometry.polygon import LinearRing

from pygooglechart import XYLineChart
import webbrowser

from pymunk.vec2d import Vec2d
from pymunk.util import *

import random

class Building:
    """ a building has a list of verticies that define it as well as
        other features.
            * a density? weight?
            * cost? (space taken up on the ground)
            * height?
    """
    def __init__(self, verticies):
        self.verticies = verticies  # a list of verticies defining this building

        self.poly = [Vec2d(v) for v in verticies] # a polygon reprsentation of the building
        self.triangles = triangulate(self.poly)
        self.convexes = convexise(self.triangles) # convexes representing the building shape

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

    def get_poly(self):
        return self.poly

    def get_triangles(self):
        return self.triangles

    def get_convexes(self):
        return self.convexes

    def fitness(self):
        """ return the fitness of this particular building
        """
        return 0

    def graph(self):
        """ graph the building as a polygon using google charts
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
    def __init__(self, size, fill):
        self.size = size
        self.buildings = []
        if fill:
            self.generate()

    def generate(self):
        for n in range(self.size):
            # construct a random building and add it to the population
            self.buildings.append(random_building())

    def get_buildings(self):
        return self.buildings

    def get_size(self):
        return self.size

    def fill(self):
        return 0

    def fittest(self):
        # calculate the best building
        return 0


def generate_verticies(num_vertices):
    vert = []
    for n in range(num_vertices):
        vert.append((random.randint(20,200), random.randint(20,200))) # tuple represents a point
    return vert

def valid_poly(v):
    """ returns true if a set of vertices contructs a simple and counter-clockwise polygon
        
        simple = no edges cross each other
        counter-clockwise = in practice this seems important!

        a valid building must meet both of these criteria
    """
    poly = LinearRing(v)
    return (poly.is_simple and poly.is_ccw)

def random_building():
    num_vertices = random.randint(3, 10) # at least 3, or else is a line
    vert = generate_verticies(num_vertices)
    while not valid_poly(vert):
        # verticies need to construct counter clockwise, simple polygons
        vert = generate_verticies(num_vertices)

    # we know we have a valid set of verticies
    b = Building(vert)
    return b


# POPULATION GENERATION

# for size_of_population:
    # RANDOM BUIDLING GENERATION

# FITNESS

# CROSSOVER

# MUTATION 


# p = Population(10, True)
# buildings = p.get_buildings()
# for b in buildings:
#     b.graph()