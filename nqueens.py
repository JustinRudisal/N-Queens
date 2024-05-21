# Created by Justin Rudisal
import random
import time
from concurrent.futures import ThreadPoolExecutor

NUM_RUNS = 5
POPULATION_AMOUNT = 75

# Set to true for multithreading, but I found it becomes a hinderance if the population isn't large enough
MULTITHREADING = False

# Mutation globals for incremental mutation chances
BASE_MUTATION_PROBABILITY = 0.05
MAX_MUTATION_PROBABILITY = 0.75

# Escape globals to avoid getting stuck
# If AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING is set to -1, it will randomize entire population
# If the AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING is greater than the POPULATION_AMOUNT, it will randomize entire population
AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING = 15
ESCAPE_EVERY_X_GENERATIONS = 200

# For debugging
PRINT_CHROMOSOMES = False
PRINT_GENERATIONS = False
PRINT_ESCAPE_INDICATOR = False

# Cache for the fitness values in order to avoid recalculating a known chromsome's fitness value
fitness_cache = {}
RESET_FITNESS_CACHE_AFTER_EACH_RUN = True

# Generating random chromosomes 
def random_chromosome(): 
    return [ random.randint(1, nq) for _ in range(nq) ]

def calculate_fitnesses(chromosomes):
    results = []
    if MULTITHREADING:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(fitness, chromosomes))
    else:
        for chromosome in chromosomes:
            results.append(fitness(chromosome))
    return results

def fitness(chromosome):
    chrom_key = tuple(chromosome)
    if chrom_key in fitness_cache:
        return fitness_cache[chrom_key]

    diagonal_collisions = 0
    vertical_collisions = 0
    n = len(chromosome)

    # Check for vertical collisions (implied by repeated numbers)
    column_counts = [0] * n
    for q in chromosome:
        column_counts[q-1] += 1
    vertical_collisions = sum([count-1 for count in column_counts if count > 1])

    # Check each pair of queens for diagonal collisions
    for i in range(n):
        for j in range(i+1, n):
            if abs(chromosome[i] - chromosome[j]) == abs(i - j):
                diagonal_collisions += 1

    # Calculate the adjusted fitness score
    calculated_fitness = maxFitness - (diagonal_collisions + vertical_collisions)
    fitness_cache[chrom_key] = calculated_fitness
    return calculated_fitness

def probability(chromosome):
    return fitness_cache[tuple(chromosome)] / maxFitness

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"
        
def reproduce(x, y): #doing cross_over between two chromosomes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

def mutate(chromosome, escape_counter, escape):  
    chromosome_length = len(chromosome)
    if escape:
        queen_index = random.randint(0, chromosome_length - 1)
        new_position = random.randint(1, chromosome_length)
        chromosome[queen_index] = new_position
        if PRINT_ESCAPE_INDICATOR:
            print("Escape Triggered! Resetting escape probability to zero.")
        if escape_counter > AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING and AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING != -1:
            escape = False
        else:
            escape_counter += 1
        return chromosome, escape, escape_counter
    
    number_of_attacks = [0 for _ in range(chromosome_length)]
    for i in range(chromosome_length):
        for j in range(chromosome_length):
            if i != j:
                if chromosome[i] == chromosome[j] or abs(i - j) == abs(chromosome[i] - chromosome[j]):
                    number_of_attacks[i] += 1

    queen_with_the_most_attacks = number_of_attacks.index(max(number_of_attacks))

    minimum_number_of_attacks = float('inf')
    new_position = chromosome[queen_with_the_most_attacks]
    for row in range(1, chromosome_length + 1):
        original_position = chromosome[queen_with_the_most_attacks]
        chromosome[queen_with_the_most_attacks] = row
        attacks_at_position = sum([1 for i in range(chromosome_length) for j in range(i + 1, chromosome_length) if chromosome[i] == chromosome[j] or abs(i - j) == abs(chromosome[i] - chromosome[j])])
        if attacks_at_position < minimum_number_of_attacks:
            new_position = row
            minimum_number_of_attacks = attacks_at_position
        chromosome[queen_with_the_most_attacks] = original_position

    chromosome[queen_with_the_most_attacks] = new_position
    return chromosome, escape, escape_counter

def calculate_parameters(current_runtime, generation, escape, escape_counter, mutation_probability):
    if (generation % ESCAPE_EVERY_X_GENERATIONS == 0 and (escape_counter < AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING + 1 or AMOUNT_OF_POPULATION_TO_RANDOMIZE_WHEN_ESCAPING == -1)):
        escape = True
    if mutation_probability != MAX_MUTATION_PROBABILITY:
        mutation_probability = min(BASE_MUTATION_PROBABILITY + (MAX_MUTATION_PROBABILITY - BASE_MUTATION_PROBABILITY) * (current_runtime ** 2), MAX_MUTATION_PROBABILITY)
    return escape, mutation_probability

def genetic_queen(population, maxFitness, current_runtime, generation, escape):
    new_population = []

    best_chromosomes_size = int(0.05 * len(population))
    best_chromosomes = sorted(population, key=lambda chrom: fitness_cache[tuple(chrom)], reverse=True)[:best_chromosomes_size]
    for best_chromosome in best_chromosomes:
        new_population.append(best_chromosome)

    escape_counter = 0
    mutation_probability = BASE_MUTATION_PROBABILITY
    probabilities = [probability(n) for n in population]
    while len(new_population) < len(population):
        escape, mutation_probability = calculate_parameters(current_runtime, generation, escape, escape_counter, mutation_probability)
        x = random_pick(population, probabilities)
        y = random_pick(population, probabilities)
        child = reproduce(x, y)  
        if random.random() < mutation_probability and child not in best_chromosomes:
            child, escape, escape_counter = mutate(child, escape_counter, escape)
        if PRINT_CHROMOSOMES:
            print_chromosome(child)
        if child not in new_population:
            new_population.append(child)
        if not MULTITHREADING and fitness(child) == maxFitness:
            break
    return new_population, mutation_probability, escape


def print_chromosome(chrom):
    fitness_value = fitness_cache.get(tuple(chrom), None)
    if fitness_value is None:
        fitness_value = fitness(chrom)
    print("Chromosome = {},  Fitness = {}"
        .format(str(chrom), fitness_value))

if __name__ == "__main__":
    total_runtimes = [] 
    average_runtime = -1
    nq = int(input("Enter Number of Queens: ")) # say N = 8
    for run in range(1, NUM_RUNS + 1):
        if RESET_FITNESS_CACHE_AFTER_EACH_RUN:
            fitness_cache = {}
        print("\n---------------------------------------------")
        start_time = time.time()
        maxFitness = (nq*(nq-1))/2  
        population = [random_chromosome() for _ in range(POPULATION_AMOUNT)]
        population_fitnesses = calculate_fitnesses(population)
        print("\nMaximum fitness = {}" .format(str(maxFitness)))
        
        generation = 1

        mutation_probability = BASE_MUTATION_PROBABILITY
        current_maxFitness = 0
        while current_maxFitness != maxFitness:
            escape = False
            current_runtime = time.time() - start_time
            if PRINT_GENERATIONS:
                print(f"Current Generation: {generation}, Current Max Fitness: {current_maxFitness}, Current Runtime: {current_runtime:.2f}, Mutation Probability: {mutation_probability*100:.2f}%")
            population, mutation_probability, escape = genetic_queen(population, maxFitness, current_runtime, generation, escape)
            population_fitnesses = calculate_fitnesses(population)
            current_maxFitness = max(population_fitnesses)
            if PRINT_CHROMOSOMES:
                print("")
                print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
            generation += 1
        chrom_out = []
        end_time = time.time()
        total_time = end_time - start_time
        total_runtimes.append(total_time)
        average_runtime = sum(total_runtimes) / run
        print("Solved in Generation {}!".format(generation-1))
        for chrom in population:
            if fitness(chrom) == maxFitness:
                print("")
                print("One of the solutions: ")
                chrom_out = chrom
                print_chromosome(chrom)
                
        board = []

        for x in range(nq):
            board.append(["x"] * nq)
            
        for i in range(nq):
            board[nq-chrom_out[i]][i]="Q"

        def print_board(board):
            for row in board:
                print (" ".join(row))
                
        print()
        print_board(board)
        print("\nTotal runtime: {:.2f} seconds".format(total_time))

    print("\n---------------------------------\n\nAverage Runtime over {} runs: {:.2f} seconds".format(NUM_RUNS, average_runtime))