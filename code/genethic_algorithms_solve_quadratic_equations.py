import random

# CONSTANT VARIABLES
POPULATION_SIZE = 100
CHROMOSOME_LENGTH = 8
MUTATION_RATE = 0.05
GENERATIONS = 100
A = 1
B = -2
C = 1


def decode_chromosome(chromosome):
    x = int("".join(map(str, chromosome)), 2)
    return x


def fitness(x):
    a = A
    b = B
    c = C
    return abs(a * x**2 + b * x + c)


def generate_random_population(population_size, chromosome_length):
    population = [
        [random.randint(0, 1) for _ in range(chromosome_length)]
        for _ in range(population_size)
    ]

    return population


def selection(population):
    population_with_fitness = [
        (chromosome, fitness(decode_chromosome(chromosome)))
        for chromosome in population
    ]

    sorted_population = sorted(
        population_with_fitness,
        key=lambda x: x[1]
    )

    return [
        chromosome for chromosome, _ in sorted_population[:len(population) // 2]
    ]


def crossover(parent_1, parent_2):
    crossover_point = random.randint(1, len(parent_1) - 1)
    child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
    child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]
    return child_1, child_2


def mutation(chromosome, mutation_rate):
    new_child = [
        bit if random.random() > mutation_rate else 1 - bit
        for bit in chromosome
    ]
    return new_child


def genetic_algorithm(
        population_size,
        chromosome_length,
        generations,
        mutation_rate
):
    populations = generate_random_population(population_size, chromosome_length)

    for generation in range(generations):
        populations_with_fitness = selection(populations)
        # print(f"Generation {generation + 1}: Best fitness - {fitness(decode_chromosome(populations_with_fitness[0]))}")

        new_population = []

        for _ in range(population_size):
            parent_1, parent_2 = random.sample(populations_with_fitness, 2)

            child_1, child_2 = crossover(parent_1, parent_2)

            new_population.append(mutation(child_1, MUTATION_RATE))
            new_population.append(mutation(child_2, MUTATION_RATE))

        populations = new_population

    best_chromosome = min(
        populations,
        key=lambda chromosome: fitness(decode_chromosome(chromosome))
    )

    return decode_chromosome(best_chromosome)

if __name__ == "__main__":
    solution = genetic_algorithm(
        POPULATION_SIZE,
        CHROMOSOME_LENGTH,
        GENERATIONS,
        MUTATION_RATE
    )

    print(f"result: {solution}")
