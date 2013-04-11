import math
import random
import webbrowser

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

    def graph(self):
        ''' graphs the map using google graph api '''
        ms = self.map_size
        chart = ScatterChart(ms, ms, x_range=(0, ms), y_range=(0, ms))
        xdata = [c.getx() for c in self.cities]
        ydata = [c.gety() for c in self.cities]
        chart.add_data(xdata)
        chart.add_data(ydata)
        webbrowser.open(chart.get_url())

class tour:
    # a tour is a chromosome...

    def __init__(self, amap):
        ''' initially, a tour order is a random shuffle of the cities in the map 
            PLUS the first element in the tour -- we have to go back to the start '''
        city_shuffle = amap.get_cities()
        random.shuffle(city_shuffle)
        self.tour_order = city_shuffle.append(city_shuffle[0])
        self.map_size = amap.get_map_size()

    def get_order(self):
        return self.tour_order

    def fitness(self):
        ''' returns fitness of this tour'''
        city_pairs = zip(self.tour_order[:-1], self.tour_order[1:])
        pair_distances = [x.getdistance(y) for (x,y) in city_pairs]
        fitness = sum(pair_distances)
        return fitness

    def graph(self):
        ms = self.map_size
        chart = XYLineChart(ms, ms, x_range=(0, ms), y_range=(0, ms))
        # add x coords
        # add y coords

def xy_rect():

    chart = XYLineChart(100,100, x_range=(0, 100), y_range=(0, 100))
    chart.add_data([10, 80, 80, 10, 10])  # x coords
    chart.add_data([10, 10, 90, 90, 10])  # y coords
    webbrowser.open(chart.get_url())


def rand_map(num_cities, map_size):
    ''' generates a random map with a number of cities and a size in px '''
    m = amap(map_size)
    i = 0
    while (i <= num_cities):
        m.add_city()
        i+=1
    return m


