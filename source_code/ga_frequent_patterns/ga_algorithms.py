from create_candidate import candidate
from constant import *
import random


def is_exists(transaction, candidate, item_candidate):
    i = 0
    n = len(candidate)
    m = len(transaction)

    while i < n and candidate[i] == 0:
        i += 1  # tìm nhiễm sắc thể đầu tiên = 1

    if i == n:
        return False  # nếu không tìm thấy

    j = 0  # duyệt từ đầu transaction
    while i < n:  # duyệt trên candidate
        while (
            j < m and transaction[j] != item_candidate[i]
        ):  # trong khi chưa có xuất hiện ở transaction
            j += 1

        if j == m:
            return False  # nếu không tìm thấy

        i += 1
        j += 1  # qua phần tử kế

        while i < n and candidate[i] == 0:
            i += 1

    return True


def fitness_function(dataset, candidate, item_candidate):
    count = 0

    for data in dataset:
        if is_exists(data, candidate, item_candidate):
            count += 1

    return count


# Hàm lai ghép hai cá thể để tạo ra con cái
def crossover(parent1, parent2):
    crossover_point1 = random.randint(1, len(parent1) // 2)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)

    child1 = (
        parent1[:crossover_point1]
        + parent2[crossover_point1:crossover_point2]
        + parent1[crossover_point2:]
    )

    child2 = (
        parent2[:crossover_point1]
        + parent1[crossover_point1:crossover_point2]
        + parent2[crossover_point2:]
    )

    return child1, child2


# Hàm đột biến một cá thể
def mutate(individual):
    mutation_point = random.randint(0, len(individual) - 1)
    individual[mutation_point] = (
        1 - individual[mutation_point]
    )  # Đổi giá trị 0 thành 1 hoặc 1 thành 0


# Chuyển từ transaction sang mảng bit
def convert_to_bit(individual, individual_size):
    bit_arr = [0 for _ in range(individual_size)]

    for i in individual:
        bit_arr[i - 1] = 1

    return bit_arr


# Khởi tạo quần thể ban đầu
def generate_population(population_size, individual_size, dataset):
    dataset_copy = dataset.copy()
    population = []

    for _ in range(population_size):
        pos = random.randint(0, len(dataset_copy) - 1)
        individual = dataset_copy[pos]

        population.append(convert_to_bit(individual, individual_size))
        dataset_copy.remove(individual)

    return population


def convert_bit_to_transaction(individual):
    transaction = []

    for i in range(len(individual)):
        if individual[i] == 1:
            transaction.append(i + 1)

    return transaction


def find_frequent_item_sets(population, dataset, support_count, item_candidate):
    fitness_scores = [
        fitness_function(dataset, individual, item_candidate)
        for individual in population
    ]

    frequent_item_sets = []

    for i in range(len(fitness_scores)):
        if fitness_scores[i] >= support_count:
            frequent_item_sets.append(
                (convert_bit_to_transaction(population[i]), fitness_scores[i])
            )

    return frequent_item_sets


def select(population, fitness_scores, support_count):
    sorted_indices = sorted(
        range(len(fitness_scores)), key=lambda k: fitness_scores[k], reverse=True
    )

    selected = []
    for i in sorted_indices:
        if fitness_scores[i] < support_count:
            break
        selected.append(population[i])

    return selected


def random_selected(selected_parents):
    length = len(selected_parents)
    half_length = length // 2

    parent1_index = random.randint(0, half_length - 1)
    parent2_index = random.randint(half_length, length - 1)

    parent1 = selected_parents[parent1_index]
    parent2 = selected_parents[parent2_index]

    return parent1, parent2


# kiểm tra trùng
def check_for_duplicates(child, next_generation):
    for individual in next_generation:
        return individual == child


def generate_population_bit_array(population_size, item_candidate):
    population = []

    for _ in range(1, population_size + 1):
        r = random.randint(1, item_candidate)
        binary_string = format(r, f"0{item_candidate}b")
        individual = []

        for c in binary_string:
            if c == "1":
                individual.append(1)
            else:
                individual.append(0)

        population.append(individual)

    return population


def copy_population(population):
    new_population = []

    for individual in population:
        new_population.append(individual)

    return new_population


def genetic_algorithms(
    generations,
    population_size,
    dataset,
    support_count,
    crossover_probability,
    mutation_probability,
):

    item_candidate = candidate(dataset, support_count)
    population = generate_population_bit_array(population_size, len(item_candidate))

    for _ in range(generations):
        fitness_scores = [
            fitness_function(dataset, individual, item_candidate)
            for individual in population
        ]

        selected_parents = select(population, fitness_scores, support_count)

        next_generation = copy_population(selected_parents)

        while len(next_generation) < population_size:
            parent1, parent2 = random_selected(selected_parents)

            if random.random() < crossover_probability:
                child1, child2 = crossover(parent1, parent2)

                next_generation.append(child1)
                next_generation.append(child2)

        # Đột biến ngẫu nhiên
        for individual in next_generation:
            if random.random() < mutation_probability:
                mutate(individual)
        # Cập nhật quần thể mới
        population = copy_population(next_generation)

    frequent_item_sets = find_frequent_item_sets(
        population, dataset, support_count, item_candidate
    )

    return frequent_item_sets


if __name__ == "__main__":

    all_frequent_item_sets = genetic_algorithms(
        GENERATIONS,
        POPULATION_SIZE,
        DATASET_FILE,
        SUPPORT_COUNT,
        CROSSOVER_PROBABILITY,
        MUTATION_PROBABILITY,
    )
    

    print(all_frequent_item_sets)


