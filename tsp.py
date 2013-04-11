import math
import random
import webbrowser
import copy

from pygooglechart import ScatterChart
from pygooglechart import XYLineChart

''' Initial research: practicing writing genetic algorithms
    This program evolves (sub-optimal of course) solutions to the classic Traveling 
    Salesman Problem. '''

class city:
    def __init__(self, map_size):
        self.x = random.randint(0, map_size)
        self.y = random.randint(0, map_size)

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getdistance(self, dst):
        xd = math.fabs(self.x - dst.getx())
        yd = math.fabs(self.y - dst.gety())
        distance = math.sqrt(pow(xd, 2) + pow(yd, 2))
        return distance


class amap:

    def __init__(self, map_size):
        self.cities = []
        self.map_size = map_size

    def add_city(self):
        c = city(self.map_size)
        self.cities.append(c)

    def get_cities(self):
        return self.cities

    def get_map_size(self):
        return self.map_size
    
    def print_cities(self):
        i = 0
        for c in self.cities:
            print 'city %d:  (%d, %d)' % (i, c.getx(), c.gety())
            i+=1

    def create_tour(self):
        cities = copy.deepcopy(self.cities)
        random.shuffle(cities)
        cities.append(cities[0])
        ms = copy.deepcopy(self.map_size)
        return tour(cities, ms)  

    def graph(self):
        ''' graphs the map using google graph api '''
        ms = copy.deepcopy(self.map_size)
        chart = ScatterChart(ms, ms, x_range=(0, ms), y_range=(0, ms))
        cs = copy.deepcopy(self.cities)
        xdata = [c.getx() for c in cs]
        ydata = [c.gety() for c in cs]
        chart.add_data(xdata)
        chart.add_data(ydata)
        webbrowser.open(chart.get_url())

class tour:

    def __init__(self, tour_order, map_size):
        ''' initially, a tour order is a random shuffle of the cities in the map 
            PLUS the first element in the tour -- we have to go back to the start '''
        self.tour_order = tour_order
        self.map_size = map_size

    def get_order(self):
        return self.tour_order

    def fitness(self):
        ''' returns fitness of this tour'''
        city_pairs = zip(self.tour_order[:-1], self.tour_order[1:])
        pair_distances = [x.getdistance(y) for (x,y) in city_pairs]
        fitness = sum(pair_distances)
        return fitness

    def graph(self):        
        ms = copy.deepcopy(self.map_size)
        chart = XYLineChart(ms, ms, x_range=(0, ms), y_range=(0, ms))
        to = copy.deepcopy(self.tour_order)
        xcoords = [c.getx() for c in to]
        ycoords = [c.gety() for c in to]
        chart.add_data(xcoords)
        chart.add_data(ycoords)

        webbrowser.open(chart.get_url())

class population:

    def __init__(self, size):
        m = rand_map(10, 250)
        p = []
        i = 0
        while (i < size):
            p.append(m.create_tour())
            i+=1
        self.pop = p

    def get_pop(self):
        return self.pop

    def fittest(self):
        best = float('inf')
        best_so_far = 0
        for p in self.pop:
            fit = p.fitness()
            if (best > fit):
                best = fit
                best_so_far = p
        return best_so_far


def rand_map(num_cities, map_size):
    ''' generates a random map with a number of cities and a size in px '''
    m = amap(map_size)
    i = 0
    while (i <= num_cities):
        m.add_city()
        i+=1
    return m



p = population(100)
f = p.fittest()
f.graph()




