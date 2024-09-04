import random
import math

# Parameter GA
population_size = 100
max_generations = 100
Pc = 0.8  # Crossover probability
Pm = 0.05  # Mutation probability

# domain x1 and x2
min_val, max_val = -10, 10

# Panjang bit setiap individu
bit_count = 16

# Fungsi fitness
def fitness_function(x1, x2):
    return -(math.sin(x1) * math.cos(x2) + 4/5 * math.exp(1 - math.sqrt(x1**2 + x2**2)))

# Convert binary to decimal
def binary_to_float(binary, min_val, max_val):
  val1 = 0
  val2 = 0
  for i in range(bit_count):
    val1 = val1 + (int(binary[i]) * (2 ** (-1 * i+1)))

    val2 = val2 + (2 ** (-1 * i+1))
  return min_val + (val1 * (max_val - min_val) / val2)

def create_population():
  return [''.join(random.choice('01') for _ in range(2 * bit_count)) for _ in range(population_size)]

# Evaluasi nilai fitness populasi
def evaluate_population(population):
    fitness_values = []
    for ind in population:
        x1_binary, x2_binary = ind[:bit_count], ind[bit_count:]
        x1 = binary_to_float(x1_binary, min_val, max_val)
        x2 = binary_to_float(x2_binary, min_val, max_val)
        fitness_values.append(-fitness_function(x1, x2))
    return fitness_values

# Seleksi parent menggunakan Roulette Wheel Selection
def select_parents(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

# Single-point crossover
def crossover(parent1, parent2):
    if random.random() < Pc:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2

# Mutation
def mutate(individual):
    mutated = list(individual)
    for i in range(len(mutated)):
        if random.random() < Pm:
            mutated[i] = '0' if mutated[i] == '1' else '1'
    return ''.join(mutated)

population = create_population()

for generation in range(max_generations):
    fitness_values = evaluate_population(population)
    population_with_fitness = list(zip(population, fitness_values))
    population_with_fitness.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness ascending

    best_individuals_count = max(int(0.1 * population_size), 1)  #Menentukan banyaknya individu yang akan dihasilkan dari seleksi survivor elitism

    best_individuals = [x[0] for x in population_with_fitness[:best_individuals_count]]

    #Memasukkan hasil elitism ke populasi baru
    new_population = best_individuals[:]

    while len(new_population) < population_size:
        # Parent selection
        parents = select_parents(population, fitness_values)

        # Crossover
        offspring1, offspring2 = crossover(parents[0], parents[1])

        # Mutation
        offspring1 = mutate(offspring1)
        offspring2 = mutate(offspring2)

        #Memasukkan individu baru ke kumpulan populasi baru
        new_population.extend([offspring1, offspring2])

    #Mendeklarasi generasi baru
    population = new_population

fitness_values = evaluate_population(population)
population_with_fitness = list(zip(population, fitness_values))
population_with_fitness.sort(key=lambda x: x[1], reverse=True)
best_solution = population_with_fitness[0][0]
x1_final_binary, x2_final_binary = best_solution[:bit_count], best_solution[bit_count:]
x1_final = binary_to_float(x1_final_binary, min_val, max_val)
x2_final = binary_to_float(x2_final_binary, min_val, max_val)
best_fitness = population_with_fitness[0][1]


print("kromosom terbaik : ", best_solution)
print("x1 =", x1_final)
print("x2 =", x2_final)
print("best fitness =", best_fitness)
print("Minimum function value =", fitness_function(x1_final, x2_final))