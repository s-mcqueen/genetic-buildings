import math, random, webbrowser, copy

from pygooglechart import ScatterChart
from pygooglechart import XYLineChart

''' Initial research: practicing writing genetic algorithms
    This program evolves (sub-optimal of course) solutions to the classic Traveling 
    Salesman Problem. '''

MAP_SIZE = 250
MUTATION_RATE = 10

class city:
    def __init__(self):
        self.x = random.randint(0, MAP_SIZE)
        self.y = random.randint(0, MAP_SIZE)

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getdistance(self, dst):
        xd = math.fabs(self.x - dst.getx())
        yd = math.fabs(self.y - dst.gety())
        distance = math.sqrt(pow(xd, 2) + pow(yd, 2))
        return distance

    def print_city(self):
        print '(x,y):  (%d, %d)' % (self.x, self.y)


class amap:

    def __init__(self):
        self.cities = []


    def add_city(self):
        self.cities.append(city())

    def get_cities(self):
        return self.cities
    
    def print_cities(self):
        i = 0
        for c in self.cities:
            print 'city %d:  (%d, %d)' % (i, c.getx(), c.gety())
            i+=1

    def create_tour(self):
        cities = copy.deepcopy(self.cities)
        random.shuffle(cities)

        return tour(cities)  

    def graph(self):
        ''' graphs the map using google graph api '''

        chart = ScatterChart(MAP_SIZE, MAP_SIZE, 
                            x_range=(0, MAP_SIZE), y_range=(0, MAP_SIZE))
        cs = copy.deepcopy(self.cities)

        xdata = [c.getx() for c in cs]
        ydata = [c.gety() for c in cs]
        chart.add_data(xdata)
        chart.add_data(ydata)
        webbrowser.open(chart.get_url())

class tour:

    def __init__(self, tour_order):
        ''' initially, a tour order is a random shuffle of the cities in the map 
            PLUS the first element in the tour -- we have to go back to the start '''
        self.tour_order = tour_order

    def get_order(self):
        return self.tour_order

    def get_length(self):
        return len(self.tour_order)

    def add_stop(self, stop):
        self.tour_order.append(stop)

    def print_cities(self):
        i = 0
        for c in self.tour_order:
            print 'city %d:  (%d, %d)' % (i, c.getx(), c.gety())
            i+=1

    def fitness(self):
        ''' returns fitness of this tour'''

        to = copy.deepcopy(self.tour_order)
        
        # add 1st city at the end for fitness purposes
        to.append(to[0])

        city_pairs = zip(to[:-1], to[1:])
        pair_distances = [x.getdistance(y) for (x,y) in city_pairs]
        fitness = sum(pair_distances)
        return fitness

    def graph(self):     

        to = copy.deepcopy(self.tour_order)

        # add 1st city at the end for graphing purposes
        to.append(to[0])

        chart = XYLineChart(MAP_SIZE, MAP_SIZE, 
                            x_range=(0, MAP_SIZE), y_range=(0, MAP_SIZE))
        xcoords = [c.getx() for c in to]
        ycoords = [c.gety() for c in to]
        chart.add_data(xcoords)
        chart.add_data(ycoords)

        webbrowser.open(chart.get_url())

class population:

    def __init__(self, size, fill):
        self.pop_size = size
        self.pop = []
        if fill:        
            m = rand_map(10)
            p = []
            i = 0
            while (i < size):
                p.append(m.create_tour())
                i+=1
            self.pop = p

    def add_tour(self, tour):
        self.pop.append(tour)

    def get_pop(self):
        return self.pop

    def get_size(self):
        return self.pop_size

    def fittest(self):
        best = float('inf')
        best_so_far = 0
        for p in self.pop:
            fit = p.fitness()
            if (best > fit):
                best = fit
                best_so_far = p
        return best_so_far


def rand_map(num_cities):
    ''' generates a random map with a number of cities and a size in px '''
    m = amap()
    i = 0
    while (i <= num_cities):
        m.add_city()
        i+=1
    return m



def tournament(pop, size):

    tournament = population(size, False)
    for s in range(size):
        tour = random.choice(pop)
        tournament.add_tour(tour)

    f = tournament.fittest()

    return f


# sections is wrong -- it needs to check if cities are in the tour, so 
# it doesn't add cities twice. It also needs to make sure that all cities make it
# the tour
def sections(parent1, parent2):
    order1 = copy.deepcopy(parent1.get_order())
    order2 = copy.deepcopy(parent2.get_order())

    start_i = 1
    end_i = 0
    while (start_i >= end_i):
        c1 = random.choice(order1)
        c2 = random.choice(order1)
        start_i = order1.index(c1)
        end_i = order1.index(c2)

    # sections are part
    parent1_section = order1[start_i:end_i]
    parent2_section = order2[end_i:] + order2[:start_i]

    parent1.print_cities()
    print '----'

    for c in parent1_section:
        c.print_city()

    print '------------'
    parent2.print_cities()
    print '----'

    for c in parent2_section:
        c.print_city()

    return (parent1_section, parent2_section)

# parents are tours
def crossover(parent1, parent2):

    t1 = copy.deepcopy(parent1)
    t2 = copy.deepcopy(parent2)

    s1, s2 = sections(t1, t2)
    child_order = s1 + s2

    child = tour(child_order)
    return child


def mutate(pop):
    pop_size = pop.get_size()

    # for tours in range(pop_size):
        # if random num < MUTATION_RATE:
            # select two random cities and swap them

    # return population
    return 0


def evolve(pop, pop_size):
    new_pop = population(pop_size, False)

    pop_size = pop.get_size()
    new_pop_size = new_pop.get_size()

    for n in range(new_pop_size):
        parent1 = tournament(pop_size, 20)
        parent2 = tournament(pop_size, 20)
        child = crossover(parent1, parent2)
        # add child to new population (add_tour)

    mutate(new_pop)
    return new_pop

def evolution(pop_size, iterations):
    p = population(pop_size, True)
    for x in range(iterations):
        evolve(p, pop_size)

    f = p.fittest()
    f.graph()



# m = rand_map(5)
# t = m.create_tour()
# j = m.create_tour()
# t.graph()
# j.graph()

# child = crossover(t,j)

# child.graph()
# print '=========='
# child.print_cities()
