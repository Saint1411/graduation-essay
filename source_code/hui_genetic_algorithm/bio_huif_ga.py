import math
import bitarray
import random

class Pair:
    def __init__(self):
        self.item = 0
        self.utility = 0

class ChroNode:
    def __init__(self, length=0):
        self.chromosome = bitarray.bitarray(length)
        self.fitness = 0
        self.rfitness = 0.0
        self.rank = 0

    def deepcopy(self, temp_chro_node):
        self.chromosome = temp_chro_node.chromosome.copy()
        self.fitness = temp_chro_node.fitness
        self.rfitness = temp_chro_node.rfitness
        self.rank = temp_chro_node.rank

    def calculate_fitness(self, k, temp_list, twu_pattern, database):
        if k == 0:
            return
        fitness = 0
        for m in range(len(temp_list)):
            p = temp_list[m]
            i, j, q, temp, sum = 0, 0, 0, 0, 0
            while q < len(database[p]) and i < len(self.chromosome):
                if self.chromosome[i]:
                    if database[p][q].item == twu_pattern[i]:
                        sum += database[p][q].utility
                        i += 1
                        q += 1
                        temp += 1
                    else:
                        q += 1
                else:
                    i += 1
            if temp == k:
                fitness += sum
        self.fitness = fitness

    def __lt__(self, other):
        return -(self.fitness - other.fitness)

class HUI:
    def __init__(self, itemset, fitness):
        self.itemset = itemset
        self.fitness = fitness

class Item:
    def __init__(self, item=0):
        self.item = item
        self.tids = bitarray.bitarray()

def pev_check(temp_ba_individual, list, items, database):
    temp_list = [i for i, bit in enumerate(temp_ba_individual.chromosome) if bit]
    if not temp_list:
        return False
    temp_bitset = items[temp_list[0]].tids.copy()
    mid_bitset = temp_bitset.copy()
    for i in range(1, len(temp_list)):
        temp_bitset &= items[temp_list[i]].tids
        if temp_bitset.any():
            mid_bitset = temp_bitset.copy()
        else:
            temp_bitset = mid_bitset.copy()
            temp_ba_individual.chromosome[temp_list[i]] = False
    if not temp_bitset.any():
        return False
    list.extend(i for i, bit in enumerate(temp_bitset) if bit)
    return True

def calculate_rfitness(population):
    sum = 0
    temp = 0
    for node in population:
        sum += node.fitness
    for node in population:
        temp += node.fitness
        node.rfitness = temp / sum

def select_chromosome(population):
    rand_num = random.random()
    for i, node in enumerate(population):
        if i == 0:
            if 0 <= rand_num <= node.rfitness:
                return 0
        elif population[i - 1].rfitness < rand_num <= node.rfitness:
            return i