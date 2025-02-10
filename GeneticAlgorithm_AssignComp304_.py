import random

# Parameters
population_size = 50
generations = 1000
crossover_rate = 0.8
mutation_rate = 0.1

def read_performance_matrix(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split(',')))
            matrix.append(row)
    return matrix

def generate_chromosome(num_tasks, num_persons):
    return random.sample(range(num_persons), num_tasks)

def fitness(chromosome, performance_matrix):
    total_score = 0
    for task, person in enumerate(chromosome):
        total_score += performance_matrix[person][task]
    return total_score

# Tournament selection
def selection(population, scores):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(range(len(population)), 3)
        best_idx = max(tournament, key=lambda idx: scores[idx])
        selected.append(population[best_idx])
    return selected

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

def mutate(chromosome):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(chromosome)), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome

# Genetic Algorithm
def genetic_algorithm(performance_matrix):
    num_tasks = len(performance_matrix[0])  # Number of tasks (columns)
    num_persons = len(performance_matrix)    # Number of persons (rows)
    
    population = [generate_chromosome(num_tasks, num_persons) for _ in range(population_size)]
    best, best_eval = population[0], 0

    for generation in range(generations):
        scores = [fitness(chromosome, performance_matrix) for chromosome in population]
        for i in range(len(population)):
            if scores[i] > best_eval:
                best, best_eval = population[i], scores[i]
                print(f"> Generation {generation}, new best: {best}, Fitness: {best_eval}")

        selected = selection(population, scores)
        children = []
        while len(children) < population_size:
            p1, p2 = random.choice(selected), random.choice(selected)
            if random.random() < crossover_rate:
                offspring1, offspring2 = crossover(p1, p2)
                children.append(mutate(offspring1))
                if len(children) < population_size:
                    children.append(mutate(offspring2))
            else:
                children.append(mutate(p1))
                if len(children) < population_size:
                    children.append(mutate(p2))

        population = children

    print(f"Best solution found: {best}, Fitness: {best_eval}")

def main():
    performance_matrix = read_performance_matrix('Scores.txt')
    genetic_algorithm(performance_matrix)

if __name__ == "__main__":
    main()
