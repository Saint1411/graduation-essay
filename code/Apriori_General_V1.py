def load_data():
    # Hàm này trả về một danh sách các bộ dữ liệu mẫu
    '''return [
        [1, 7, 8],
        [1, 2, 6, 7, 8],
        [1, 2, 6, 7],
        [1, 7, 8],
        [3, 4, 5, 6, 8],
        [1, 4, 5]
    ]
    '''
    return [
        ['a', 'b', 'e', 'g'],
        ['a', 'c', 'd', 'f'],
        ['a', 'b', 'g'],
        ['b', 'c', 'd', 'e', 'g'],
        ['a', 'c', 'e', 'f']
    ]
    
def create_candidates(prev_candidates, k):
    candidates = []
    n = len(prev_candidates)

    for i in range(n):
        for j in range(i + 1, n):
            # Kết hợp hai tập hợp nếu các phần tử đầu tiên (k-2) của chúng giống nhau
            if prev_candidates[i][:k-2] == prev_candidates[j][:k-2]:
                candidate = list(set(prev_candidates[i]) | set(prev_candidates[j]))
                candidate.sort()
                candidates.append(candidate)

    return candidates

def support_count(dataset, candidate):
    count = 0
    for data in dataset:
        if set(candidate).issubset(set(data)):
            count += 1
    return count/len(dataset)

def apriori(dataset, min_support):
    candidates = []
    frequent_itemsets = []
    k = 1

    while True:
        if k == 1:
            candidates = [[item] for item in set(item for sublist in dataset for item in sublist)]
        else:
            candidates = create_candidates(candidates, k)
        print('C',k,'= ',candidates)
        print('**********')
        frequent_candidates = []
        for candidate in candidates:
            support = support_count(dataset, candidate)
            if support >= min_support:
                frequent_itemsets.append((candidate, round(support, 2)))
                frequent_candidates.append(candidate)

        if not frequent_candidates:
            break
        print('L',k,'= ',frequent_candidates)
        print('****************')
        candidates = frequent_candidates
        k += 1

    return frequent_itemsets

if __name__ == "__main__":
    dataset = load_data()
    min_support = 0.6
    frequent_itemsets = apriori(dataset, min_support)

    print("Frequent itemsets with minimum support count of", min_support)
    for itemset, support in frequent_itemsets:
        print(itemset, ":", support)
