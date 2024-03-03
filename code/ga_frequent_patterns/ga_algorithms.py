from create_candidate import candidate
from constant import *
import random



# Hàm tính mức độ phổ biến của ỨNG VIÊN
def is_exists(transaction, candidate, item_candidate):
    i = 0
    n = len(candidate)
    m = len(transaction)

    while i < n and candidate[i] == 0: 
        i += 1 #tìm nhiễm sắc thể đầu tiên = 1

    if i == n: 
        return False #nếu không tìm thấy
    
    j = 0 #duyệt từ đầu transaction
    while i < n: #duyệt trên candidate
        while j < m and transaction[j] != item_candidate[i]: #trong khi chưa có xuất hiện ở transaction
            j += 1
            
        if j == m: 
            return False #nếu không tìm thấy
        
        i += 1
        j += 1 #qua phần tử kế
        
        while i<n and candidate[i]==0: 
            i+=1

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

    child1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
    child2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]
    
    return child1, child2

# Hàm đột biến một cá thể
def mutate(individual, next_generation):
    mutation_point = random.randint(0, len(individual) - 1)
    individual[mutation_point] = 1 - individual[mutation_point]  # Đổi giá trị 0 thành 1 hoặc 1 thành 0

# Chuyển từ transaction sang mảng bit
def convert_to_bit(individual, individual_size):
    bit_arr = [0 for _ in range(individual_size)]

    for i in individual:
        bit_arr[i-1] = 1

    return bit_arr
        
# Khởi tạo quần thể ban đầu
def generate_population(population_size, individual_size, dataset):
    datasetCopy = dataset.copy()
    population = []

    for _ in range(population_size):
        pos = random.randint(0,len(datasetCopy)-1)
        individual = datasetCopy[pos] 

        population.append(convert_bit_to_transaction(individual, individual_size))
        datasetCopy.remove(individual)

    return population

def convert_bit_to_transaction(individual):
    transaction=[]

    for i in range(len(individual)):
        if individual[i] == 1:
            transaction.append(i + 1)

    return transaction 

def find_frequent_itemsets(population, dataset, support_count, item_candidate):
    fitness_scores = [
        fitness_function(dataset, individual,item_candidate) 
        for individual in population
    ]
    frequent_itemsets=[]

    for i in range(len(fitness_scores)):
        if  fitness_scores[i] >= support_count:
            frequent_itemsets.append(
                (convert_bit_to_transaction(population[i]), fitness_scores[i])
            )
            
    return frequent_itemsets

def select(population, fitness_scores, support_count ):
    selected = []

    for i in range(len(fitness_scores)):
        if fitness_scores[i] >= support_count:
            selected.append(population[i])

    return selected

def random_selected(selected_parents):
    length = len(selected_parents)
    half_length = length // 2
    
    parent1_index = random.randint(0, half_length)
    parent2_index = random.randint(half_length + 1, length - 1)

    parent1 = selected_parents[parent1_index]
    parent2 = selected_parents[parent2_index]

    return parent1, parent2

#kiểm tra trùng
def check_for_duplicates(child, next_generation):
    for individual in next_generation:
        return individual == child

#Khởi tạo quần thể 0,1 ngẫu nhiên
def generate_bit_array(population_size, item_candidate):
    population = []
    max_number = len(item_candidate)
    i = 0

    while(i < population_size):
        individual = []

        for _ in range(max_number):
            individual.append(random.randint(0, 1))

        if sum(individual) == 0:
            continue

        if not check_for_duplicates(individual, population):
            population.append( individual)
            i += 1      
            
    return population

def generate_population_bit_array(population_size, item_candidate):
    population = []

    for _ in range(1, population_size + 1):
        r = random.randint(1, item_candidate)
        binary_string = format(r, f"0{item_candidate}b")
        individual = []

        for c in binary_string:
            if c == '1':
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

# Tiến hành tối ưu hóa HÀM GA
def genetic_algorithms(
        generations, 
        population_size, 
        dataset, 
        support_count, 
        crossover_probality,
        mutation_probality
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

            if random.random() < crossover_probality:
                child1, child2 = crossover(parent1, parent2)

                next_generation.append(child1)
                next_generation.append(child2)

        # Đột biến ngẫu nhiên
        for individual in next_generation:
            if random.random() < mutation_probality:
                mutate(individual, next_generation)

        # Cập nhật quần thể mới
        population = copy_population(next_generation)

    frequent_itemsets = find_frequent_itemsets(population, dataset, support_count,item_candidate)
    
    return frequent_itemsets 

#Thuật toán chính
def ga_slide(
        generations, 
        transactions, 
        dataset,
        population_size, 
        support_count, 
        batch,
        crossover_probality,
        mutation_probality
    ):
    all_frequent_itemsets = []
    
    for _ in range(0,len(transactions), batch):
        # window_data = transactions[i:i+window_size]
        frequent_itemsets = genetic_algorithms(
            generations, 
            population_size, 
            dataset,
            support_count,
            crossover_probality,
            mutation_probality
        )

        all_frequent_itemsets.extend(frequent_itemsets)

    return all_frequent_itemsets
    

all_frequent_itemsets = genetic_algorithms(
    GENERATIONS, 
    POPULATION_SIZE, 
    DATASET_FILE, 
    SUPPORT_COUNT,
    CROSSOVER_PROBALITY,
    MUTATION_PROBALITY
)

print(all_frequent_itemsets)
