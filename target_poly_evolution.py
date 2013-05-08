from __future__ import division

from pymunk.vec2d import Vec2d
from pymunk.util import *

from shapely.geometry.polygon import Polygon
import random


class Polypoly:

    def __init__(self, target, verticies):
        self.target = target        
        self.verticies = verticies

        # generate some random verticies
        if verticies == []:
            for n in range(4):  # random.randint(3, 10)
                v = (random.uniform(0,200), random.uniform(0,200))
                self.verticies.append(v)

        self.vectors = [Vec2d(v) for v in self.verticies]
        self.triangles = triangulate(self.vectors)
        self.convexes = convexise(self.triangles) # convexes representing the shape

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target

    def get_verticies(self):
        return self.verticies        

    def get_vectors(self):
        return self.vectors

    def get_convexes(self):
        return self.convexes

    def fitness(self):
        vect = self.vectors
        t_vect = self.target.get_vectors()

        diff = 0
        for v in range(len(vect)):
            diff += vect[v].get_dist_sqrd(t_vect[v]) 

        return diff # minimize

    def crossover(self, other):
        parent1 = self.verticies
        parent2 = other.get_verticies()
   
        start_i = 1
        end_i = 0
        while (start_i >= end_i) and (len(parent1) > end_i): 
            # while loop ensures no "backwards" sections
            v1 = random.choice(parent2)
            v2 = random.choice(parent2)
            start_i = parent2.index(v1)
            end_i = parent2.index(v2)

        parent1[start_i:end_i] = parent2[start_i:end_i]
        return Polypoly(self.target, parent1)

    def this_mutate(self):
        """ angle mutate """
        v = random.choice(self.vectors) # random vector
        v_index = self.vectors.index(v) # remember where it came from
        v.angle *= random.uniform(0, 10) # change angle randomly
        self.vectors[v_index] = v  # replace
        self.triangles = triangulate(self.vectors)
        self.convexes = convexise(self.triangles) # convexes representing the shape

        self.verticies = [(v.x, v.y) for v in self.vectors]


class Population:
    def __init__(self, size, target, fill = True):
        self.size = size
        self.polygons = []
        self.target = target
        if fill:
            self.generate()

    def generate(self):
        for n in range(self.size):
            # construct a random polygon and add it to the population
            self.polygons.append(Polypoly(self.target, []))

    def get_polygons(self):
        return self.polygons

    def add_polygon(self, poly):
        self.polygons.append(poly)
        self.size = len(self.polygons)

    def get_size(self):
        return self.size

    def get_target(self):
        return self.target

    def fittest(self):
        best = float('inf')
        best_so_far = 0
        for p in self.polygons:
            fit = p.fitness()
            if (best > fit):
                best = fit
                best_so_far = p
        return (best_so_far, best)


def run_tournament(pop, size):
    tournament = Population(size, pop.get_target(), False)

    for n in range(size):
        poly = random.choice(pop.get_polygons())
        tournament.add_polygon(poly)

    fit, fitness = tournament.fittest()
    return fit

def mutation(pop, mutation_rate):
    pop_size = pop.get_size()

    for p in pop.get_polygons():
        if (random.randint(1,100) < mutation_rate):
            p.this_mutate()

def evolve(pop, mutation_rate):

    new_pop_size = (pop.get_size() // 4)
    if (new_pop_size < 10):
        new_pop_size += 10
    new_pop = Population(new_pop_size, None, False)

    tournament_size = 10

    for n in range(new_pop_size):
        parent1 = run_tournament(pop, tournament_size)
        parent2 = run_tournament(pop, tournament_size)

        
        c1 = parent1.crossover(parent2)
        c2 = parent2.crossover(parent1)

        new_pop.add_polygon(c1)
        new_pop.add_polygon(c2)
        new_pop.add_polygon(parent1) # elitism
        new_pop.add_polygon(parent2) # elitism

    mutation(new_pop, mutation_rate)
    (a,b) =  new_pop.fittest()
    print "fit : " + str(b)
    return new_pop



