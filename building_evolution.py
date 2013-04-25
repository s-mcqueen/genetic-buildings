import shapely
from shapely.geometry.polygon import LinearRing

from pygooglechart import XYLineChart
import webbrowser

import random


# RANDOM BUILDING GENERATION

def random_building():
    num_vertices = random.randint(3, 10) # at least 3, or else is a line
    vert = []
    for n in range(num_vertices):
        vert.append((random.randint(0,15), random.randint(0,15))) # tuple

    if not valid_building(vert):
        # try again -- keep num_verticies the same

    # make it into a polygon
    # triangulate / convexise polygon (pymunk.utils)
        # put these polygons together -- this is our building


def valid_building(v):
    building = LinearRing(v)
    return building.is_simple


# POPULATION GENERATION
# for size_of_population:
    # RANDOM BUIDLING GENERATION

# FITNESS

# CROSSOVER

# MUTATION 


