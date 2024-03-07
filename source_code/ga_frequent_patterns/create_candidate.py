from dataset import CDataset


def get_support_count(dataset, candidate):
    count = 0
    for data in dataset:
        if set(candidate).issubset(set(data)):
            count += 1
    return count


def candidate(data, support_count):
    frequent_item_sets = []

    candidates = [
        [item] for item in set(item for sublist in data for item in sublist)
    ]

    for candidate in candidates:
        support = get_support_count(data, candidate)

        if support >= support_count:
            frequent_item_sets.append(candidate[0])

    return frequent_item_sets


def run():
    # Example usage:
    dataset_path = "./datasets/test_dataset.txt"
    data = CDataset(dataset_path).get_transactions
    """[
        ['bread', 'milk', 'eggs'],
        ['milk', 'eggs'],
        ['bread', 'diapers', 'beer', 'eggs'],
        ['bread', 'milk', 'diapers', 'beer'],
        ['bread', 'milk', 'diapers', 'eggs']
    ]"""

    min_support = 0.5

    frequent_item_sets = candidate(data, min_support)
    print("Frequent itemsets with sliding window:")
    print(frequent_item_sets)


if __name__ == "__main__":
    run()
