import math
import random

def f(x, y):
    return 15 + x*math.cos(2*math.pi*x) + y*math.cos(14*math.pi*y)

x_interval = (-3.1, 12.1)
y_interval = (4.1, 5.8)

def create_individual():
    x = random.uniform(x_interval[0], x_interval[1])
    y = random.uniform(y_interval[0], y_interval[1])
    return (x, y)

def mutate_individual(individual, mutation_rate):
    if random.random() < mutation_rate:
        x = individual[0] + random.uniform(-0.1, 0.1)
        y = individual[1] + random.uniform(-0.1, 0.1)
        x = max(min(x, x_interval[1]), x_interval[0])
        y = max(min(y, y_interval[1]), y_interval[0])
        return (x, y)
    else:
        return individual

def crossover(parent1, parent2, crossover_rate, crossover_type):
    if random.random() < crossover_rate:
        if crossover_type == "one_point":
            x = (parent1[0] + parent2[0]) / 2
            y = (parent1[1] + parent2[1]) / 2
        elif crossover_type == "two_points":
            cut_point = random.uniform(0.25, 0.75)
            x = parent1[0] * cut_point + parent2[0] * (1 - cut_point)
            y = parent1[1] * cut_point + parent2[1] * (1 - cut_point)
        return (x, y)
    else:
        return parent1 if random.random() < 0.5 else parent2
def tournament_selection(population, fitnesses, tournament_size):
    selected_indices = random.sample(range(len(population)), tournament_size)
    best_index = max(selected_indices, key=lambda idx: fitnesses[idx])
    return population[best_index]

def roulette_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    r = random.random() * total_fitness
    idx = 0
    while r > 0:
        r -= fitnesses[idx]
        idx += 1
    return population[idx - 1]

def genetic_algorithm(pop_size, mutation_rate, crossover_rate, generations, selection_method, tournament_size=None, elitism_size=1,crossover_type ="two_point"):
    # Initialize population
    population = [create_individual() for _ in range(pop_size)]

    for gen in range(generations):
        # Evaluate fitness
        fitnesses = [f(individual[0], individual[1]) for individual in population]

        # Select parents
        if selection_method == "tournament":
            select = lambda: tournament_selection(population, fitnesses, tournament_size)
        elif selection_method == "roulette":
            select = lambda: roulette_selection(population, fitnesses)

        # Elitism
        elite_indices = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)[:elitism_size]
        new_population = [population[i] for i in elite_indices]

        # Generate offspring
        while len(new_population) < pop_size:
            parent1 = select()
            parent2 = select()
            offspring = crossover(parent1, parent2, crossover_rate, crossover_type)  # include crossover_type here
            offspring = mutate_individual(offspring, mutation_rate)
            new_population.append(offspring)

        population = new_population

    best_individual = max(population, key=lambda x: f(x[0], x[1]))
    return best_individual

if __name__ == "__main__":
    pop_size = 750
    mutation_rate = 0.1
    crossover_rate = 0.85
    generations = 300
    selection_method = "tournament"  # "roulette" or "tournament"
    tournament_size = 15
    elitism_size = 1
    crossover_type = "one_point"  # "two_points" or "two_points"
#39, 12 e 5
    best_individual = genetic_algorithm(
        pop_size=pop_size,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
        generations=generations,
        selection_method=selection_method,
        tournament_size=tournament_size,
        elitism_size=elitism_size,
        crossover_type=crossover_type  # include crossover_type here
    )

    print(f"Best individual found: {best_individual}")
    print(f"Function value at this point: {f(best_individual[0], best_individual[1])}")
