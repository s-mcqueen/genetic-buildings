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
        self.pop = []
        if fill:        
            m = rand_map(10)
            p = []
            i = 0
            while (i < size):
                p.append(m.create_tour())
                i+=1
            self.pop = p
        self.size = len(self.pop)
        
    def add_tour(self, tour):
        self.pop.append(tour)
        self.size = len(self.pop)

    def get_pop(self):
        return self.pop

    def get_size(self):
        return self.size

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

    tour_list = pop.get_pop()

    for s in range(size):
        tour = random.choice(tour_list)
        tournament.add_tour(tour)

    f = tournament.fittest()

    return f


def same_city(c1, c2):
    return (c1.getx() == c2.getx()) and (c1.gety() == c2.gety())

def city_not_in_list(c, lst):
    for l in lst:
        if same_city(c, l):
            return False
    return True


def crossover(parent1, parent2):
    
    child = tour([]) # send an empty tour
    p1 = copy.deepcopy(parent1)
    p2 = copy.deepcopy(parent2)

    # choose one of these tours to select a path from
    if (random.randint(1,2) == 1):
        chosen = p1.get_order()
        other = p2.get_order()
    else:
        chosen = p2.get_order()
        other = p1.get_order()

    # randomly choose a start and end index such that start < end
    start_i = 1
    end_i = 0
    while (start_i >= end_i):
        c1 = random.choice(chosen)
        c2 = random.choice(chosen)
        start_i = chosen.index(c1)
        end_i = chosen.index(c2)

    # grab the random path from the tour we chose
    rand_path = chosen[start_i:end_i]
    for c in rand_path:
        c.print_city()
        child.add_stop(c)

    print '------'

    for s in other:
        if city_not_in_list(s, child.get_order()):
            s.print_city()
            child.add_stop(s)
    return child


def mutate(pop):
    pop_size = pop.get_size()

    # for tours in range(pop_size):
        # if random num < MUTATION_RATE:
            # select two random cities and swap them

    # return population
    return 0


def evolve(pop):
    new_pop_size = (pop.get_size() // random.randint(1,2))

    new_pop = population(new_pop_size, False)

    for n in range(new_pop_size):
        parent1 = tournament(pop, 20)
        parent2 = tournament(pop, 20)
        for s in range(random.randint(1, 5)):
            tour = crossover(parent1, parent2)
            new_pop.add_tour(tour)

    return new_pop

def evolution(pop_size, iterations):
    p = population(pop_size, True)
    for x in range(iterations):
        evolve(p, pop_size)

    f = p.fittest()
    f.graph()


p = population(40, True)
f = p.fittest()

p1 = evolve(p)
f1 = p1.fittest()

p2 = evolve(p1)
f2 = p2.fittest()

p3 = evolve(p2)
f3 = p3.fittest()

p4 = evolve(p3)
f4 = p4.fittest()

p5 = evolve(p4)
f5 = p5.fittest()

print 'final pop size:' + str(p5.get_size())


f.graph()
f1.graph()
f2.graph()
f3.graph()
f4.graph()
f5.graph()

# m = rand_map(10)
# t = m.create_tour()
# j = m.create_tour()
# t.graph()
# j.graph()
# child = crossover(t,j)

# child.graph()
# # print '=========='
# # child.print_cities()
