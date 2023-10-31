import random
import math
from operator import attrgetter


class Individual:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        return 15 + self.x1 * math.cos(2 * math.pi * self.x1) + self.x2 * math.cos(14 * math.pi * self.x2)


def generate_initial_population(population_size):
    return [Individual(random.uniform(-3.1, 12.1), random.uniform(4.1, 5.8)) for _ in range(population_size)]


def selection(population, selection_method, tournament_size=None):
    if selection_method == "roulette":
        total_fitness = sum(individual.fitness for individual in population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual in population:
            current += individual.fitness
            if current > pick:
                return individual
    elif selection_method == "tournament":
        tournament = random.sample(population, tournament_size)
        return max(tournament, key=attrgetter('fitness'))





def mutation(individual, mutation_probability):
    if random.random() < mutation_probability:
        individual.x1 = random.uniform(-3.1, 12.1)
    if random.random() < mutation_probability:
        individual.x2 = random.uniform(4.1, 5.8)
    individual.fitness = individual.calculate_fitness()


def crossover(parent1, parent2):
    alpha = random.random()
    child_x1 = alpha * parent1.x1 + (1 - alpha) * parent2.x1
    child_x2 = alpha * parent1.x2 + (1 - alpha) * parent2.x2
    return Individual(child_x1, child_x2)

# ...

def genetic_algorithm(population_size, chromosome_size, crossover_probability, mutation_probability,
                      num_generations, selection_method, tournament_size=None, elitism_size=1):
    population = generate_initial_population(population_size)

    for generation in range(num_generations):
        new_population = sorted(population, key=attrgetter('fitness'), reverse=True)[:elitism_size]

        while len(new_population) < population_size:
            parent1 = selection(population, selection_method, tournament_size)
            parent2 = selection(population, selection_method, tournament_size)

            if random.random() < crossover_probability:
                child = crossover(parent1, parent2)
            else:
                child = random.choice([parent1, parent2])

            mutation(child, mutation_probability)
            new_population.append(child)

        population = new_population

        best_individual = max(population, key=attrgetter('fitness'))
        # Atualize a interface visual com as informações do melhor indivíduo, geração e porcentagem de erro
        # Por exemplo:
        # update_visual(best_individual, generation, error_percentage)

    return max(population, key=attrgetter('fitness'))

best_solution = genetic_algorithm(
    population_size=100,
    chromosome_size=10,
    crossover_probability=0.8,
    mutation_probability=0.01,
    num_generations=1000,
    selection_method="roulette",
    tournament_size=5,
    elitism_size=2,
)

print("Melhor solução encontrada: x1 = {}, x2 = {}, aptidão = {}".format(best_solution.x1, best_solution.x2,
                                                                         best_solution.fitness))