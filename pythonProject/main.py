class my_range:
    def __init__(self,start,end,step):
        self.start = start
        self.end = end
        self.step = step
        self.current = self.start

    def __iter__(self):
        return self
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration


        c = self.current
        self.current += self.step
        return c



for x in my_range(1,100,3):
    print(x)
