import math, random, webbrowser, copy

from pygooglechart import ScatterChart
from pygooglechart import XYLineChart
from pygooglechart import Axis


''' Initial research: practicing writing genetic algorithms
    This program evolves (sub-optimal of course) solutions to the classic Traveling 
    Salesman Problem. '''


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

    def get_city_order(self):
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
        """ returns fitness of this tour -- want to MINIMIZE this """

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

    def __init__(self, size, fill, tsp_map):
        self.tours = []
        self.tsp_map = copy.deepcopy(tsp_map)
        if fill:     
            p = []
            i = 0
            while (i < size):
                p.append(self.tsp_map.create_tour())
                i+=1
            self.tours = p
        self.size = len(self.tours)
        
    def add_tour(self, tour):
        self.tours.append(tour)
        self.size = len(self.tours)

    def get_tours(self):
        return self.tours

    def get_size(self):
        return self.size

    def get_map(self):
        return self.tsp_map

    def fittest(self):
        best = float('inf')
        best_so_far = 0
        for p in self.tours:
            fit = p.fitness()
            if (best > fit):
                best = fit
                best_so_far = p
        return (best_so_far, best)


def run_tournament(pop, size):

    tsp_map = pop.get_map()
    tour_list = pop.get_tours()

    tournament = population(size, False, tsp_map)

    for s in range(size):
        tour = random.choice(tour_list)
        tournament.add_tour(tour)

    fit, fitness =  tournament.fittest()
    return fit

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
        chosen = p1.get_city_order()
        other = p2.get_city_order()
    else:
        chosen = p2.get_city_order()
        other = p1.get_city_order()

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
        child.add_stop(c)

    for s in other:
        if city_not_in_list(s, child.get_city_order()):
            child.add_stop(s)
    return child


def mutate(pop, mutation_rate):
    pop_size = pop.get_size()

    for tour in pop.get_tours():
        if (random.randint(1,100) < mutation_rate):
            cities = tour.get_city_order()

            # select two random cities and swap them
            city1 = random.choice(cities)
            city2 = random.choice(cities)

            i = cities.index(city1)
            j = cities.index(city1)
            cities[i], cities[j] = cities[j], cities[i]

    # return population
    return pop


def evolve(pop, tsp_map, mutation_rate):

    # to keep population from growing too fast
    new_pop_size = (pop.get_size() // random.randint(1,2))
    if (new_pop_size < 10):
        new_pop_size += 10
    new_pop = population(new_pop_size, False, tsp_map)

    tournament_size = 20

    for n in range(new_pop_size):
        parent1 = run_tournament(pop, tournament_size)
        parent2 = run_tournament(pop, tournament_size)

        # parents have up to 5 children, randomly
        for s in range(random.randint(1, 2)):
            tour = crossover(parent1, parent2)
            new_pop.add_tour(tour)

    mutate(pop, mutation_rate)

    return new_pop


def graph_evolution(gens, best_per_gen):

    chart = XYLineChart(500, 500, x_range=(0, max(gens)), y_range=(0, max(best_per_gen)))

    chart.add_data(gens)
    chart.add_data(best_per_gen)

    chart.set_colours(['0000FF'])

    # x axis labels are generation numbers
    chart.set_axis_labels(Axis.BOTTOM, gens)

    webbrowser.open(chart.get_url())


def evolution(pop_size, num_gens, tsp_map, mutation_rate):
    i=0
    best_per_gen = []

    # gen 0
    p = population(pop_size, True, tsp_map)
    fit, fitness = p.fittest()
    best_per_gen.append(fitness)
    fit.graph()

    print 'initial population. size: %d, best fitness: %d' % (p.get_size(), fitness)

    for x in range(num_gens):
        i+=1
        p = evolve(p, tsp_map, mutation_rate)
        fit, fitness = p.fittest()
        best_per_gen.append(fitness)
        fit.graph()
        print 'gen: %d, size: %d, best fitness: %d' % (i, p.get_size(), fitness)

    graph_evolution(range(num_gens+1), best_per_gen)

    print "omg that's all folks!"

def rand_map(num_cities):
    ''' generates a random map with a number of cities and a size in px '''
    m = amap()
    i = 0
    while (i <= num_cities):
        m.add_city()
        i+=1
    return m


def main():
    global MAP_SIZE
    global TSP_SIZE 
    global MUTATION_RATE 

    # set globals
    MAP_SIZE = 300
    TSP_SIZE = int(raw_input("Number of cities for a random TSP: "))
    
    # set evolution params
    start_pop_size = int(raw_input("Starting population size: "))
    mutation_rate = int(raw_input("Evolution mutation rate (1-100): "))
    num_gens = int(raw_input("Number of generations: "))

    tsp_map = rand_map(TSP_SIZE)
    tsp_map.graph()
    evolution(start_pop_size, num_gens, tsp_map, mutation_rate)
    

if __name__ == "__main__":
    main()



