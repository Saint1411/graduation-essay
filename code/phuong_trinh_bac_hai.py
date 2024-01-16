import numpy as np

# Định nghĩa hàm số cần tối ưu hóa
def objective_function(x):
    a = 1
    b = -3
    c = 2
    return a * x**2 + b * x + c

# Định nghĩa hàm mục tiêu cho thuật giải di truyền
def fitness_function(x):
    return 1 / (1 + objective_function(x)**2)  # Đảo ngược để tối ưu hóa giá trị nhỏ nhất

# Hàm chọn lọc (Selection)
def selection(population, fitness_values):
    selected_indices = np.random.choice(len(population), size=len(population)//2, replace=False, p=fitness_values/fitness_values.sum())
    return population[selected_indices]

# Hàm lai ghép (Crossover)
def crossover(parents):
    crossover_point = np.random.randint(1, len(parents[0]))
    children = np.concatenate([parents[0][:crossover_point], parents[1][crossover_point:]])
    return children

# Hàm đột biến (Mutation)
def mutation(child):
    mutation_point = np.random.randint(len(child))
    mutation_value = np.random.uniform(-0.5, 0.5)
    child += mutation_value
    return child

# Thực hiện thuật giải di truyền
def genetic_algorithm(population_size=10, generations=100, mutation_probability=0.1):
    population = np.random.uniform(-10, 10, size=(population_size,))

    for generation in range(generations):
        fitness_values = np.array([fitness_function(x) for x in population])

        # Chọn lọc
        selected_population = selection(population, fitness_values)

        # Lai ghép
        new_population = []
        for _ in range(population_size // 2):
            parents = np.random.choice(selected_population, size=2, replace=False)
            children = crossover(parents)
            new_population.extend([mutation(child) for child in [children]])

        # Thay thế quần thể cũ bằng quần thể mới
        population = np.array(new_population)

    # Chọn giải pháp có fitness tốt nhất
    best_solution = population[np.argmax(fitness_values)]

    return best_solution

# Chạy thuật giải di truyền
best_solution = genetic_algorithm(population_size=10, generations=100, mutation_probability=0.1)

# In kết quả
print("Giá trị x tối ưu là:", best_solution)
print("Giá trị nhỏ nhất của hàm số là:", objective_function(best_solution))
