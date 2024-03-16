from collections import defaultdict
from element import Element
from utility_list import UtilityList
from pairl_item_utility import PairItemUtility
import time
import psutil
import random


class GeneticAlgorithm:
    def __init__(self):
        self.min_utility = 10
        self.crossover_rate = 0.8
        self.mutation_rate = 0.01
        self.individual_size = 8
        self.total_time = 0.0
        self.max_memory = 0.0
        self.hui_count = 0
        self.candidate_count = 0
        self.map_item_to_twu = {}
        self.writer = None
        self.map_fmap = defaultdict(lambda: defaultdict(int))

    def _crossover(self, parent_1, parent_2):
        cp_1 = random.randint(1, len(parent_1) // 2)
        cp_2 = random.randint(cp_1 + 1, len(parent_2) - 1)

        child_1 = f"{parent_1[:cp_1]}{parent_2[cp_1:cp_2]}{parent_1[cp_2:]}"
        child_2 = f"{parent_2[:cp_1]}{parent_1[cp_1:cp_2]}{parent_2[cp_2:]}"

        return child_1, child_2

    def _mutation(self, chromosome):
        return [
            bit if random.random() > self.mutation_rate else 1 - bit
            for bit in chromosome
        ]

    def decode_chromosome(self, chromosome):
        x = int("".join(map(str, chromosome)), 2)
        return x

    def convert_to_bit(self, individual):
        bit_arr = [0 for _ in range(self.individual_size)]

        for i in individual:
            bit_arr[i - 1] = 1

        return bit_arr


def main():
    ga_algo = GeneticAlgorithm()
    ga_algo.individual_size = 5
    bit_arr = ga_algo.convert_to_bit(40)