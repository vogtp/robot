

class ArrayFixed(object):

    def __init__(self, maxElements:int=10, defaultValue=None):
        self._defaultValue = defaultValue
        self._maxElements=maxElements
        if defaultValue:
            self.lst = [defaultValue] * maxElements
        else:
            self.lst = []

    def __call__(self):
        return self.lst

    def __getitem__(self, key):
        return self.lst[key]

    def add(self, val):
        if len(self.lst) < self._maxElements:
            self.lst.append(val) 
        else:
            self.lst[:-1] = self.lst[1:]
            self.lst[-1] = val 

    def max(self, key:callable=None):
        if key:
            return max(self.lst, key=key)
        else:
            return max(self.lst)

    
    def min(self, key:callable=None):
        if key:
            return min(self.lst, key=key)
        else:
            return min(self.lst)
    
    def sum(self, key:callable=None):
        if key:
            tot = 0
            for i in self.lst:
                tot += key(i)
            return tot
        else:
            return sum(self.lst)

    def mean(self, key:callable=None):
        return self.sum(key) / len(self.lst)