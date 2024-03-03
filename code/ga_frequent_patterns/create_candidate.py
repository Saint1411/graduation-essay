from dataset import CDataset

def get_support_count(dataset, candidate):
    count = 0
    for data in dataset:
        if set(candidate).issubset(set(data)):
            count += 1
    return count

def candidate(dataset, support_count):
    candidates = []
    frequent_itemsets = []
    
    candidates = [
        [item] for item in set(
            item for sublist in dataset for item in sublist
        )
    ]
    
    for candidate in candidates:
        support = get_support_count(dataset, candidate)

        if support >= support_count:
            frequent_itemsets.append(candidate[0])

    return frequent_itemsets

def run():
    # Example usage:
    dataset = "VD1.txt"
    data = CDataset(dataset).get_transactions
    '''[
        ['bread', 'milk', 'eggs'],
        ['milk', 'eggs'],
        ['bread', 'diapers', 'beer', 'eggs'],
        ['bread', 'milk', 'diapers', 'beer'],
        ['bread', 'milk', 'diapers', 'eggs']
    ]'''

    min_support = 0.5

    frequent_itemsets = candidate(data, min_support)
    print("Frequent itemsets with sliding window:")
    print(frequent_itemsets)

if __name__ == '__main__':
    run()    
