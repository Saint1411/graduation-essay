class CDataset:
    def __init__(self, dataset_path):
        self.transactions = []
        self.max_item = 0
        self.max_num = 0

        with open(dataset_path) as f:
            for line in f:
                if line in ["''", "#", "%", "@"]:
                    continue

                t = self.create_transaction(line)
                if len(t) > self.max_item: 
                    
                    self.max_item = len(t)

                self.transactions.append(t)

    def create_transaction(self, line):
        items_string = line.split(" ")

        items = []
        for i in range(len(items_string)):
            if items_string[i] != '\n':
                tmp = items_string[i].splitlines()
                #print(tmp)

                if len(tmp) == 0: 
                    continue

                n = int(tmp[0])

                if n > self.max_num: 
                    self.max_num = n
                    
                items.append(n)
                
        return items

    @property
    def get_transactions(self):
        return self.transactions
    
    @property
    def get_max_item(self):
        return self.max_item
    
    @property
    def get_max_num(self):
        return self.max_num
    

if __name__ == "__main__":
    print('Done..!')