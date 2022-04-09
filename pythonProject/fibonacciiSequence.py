class FibSequence:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.f1 = 0
        self.f2 = 1

    def __next__(self):
        x = self.f1 + self.f2
        self.f1 = self.f2
        self.f2 = x

        self.count += 1
        if self.count >= self.n:
            raise StopIteration
        return x

    def __iter__(self):
        return self


for c in FibSequence(10):
    print(c)

fib = FibSequence(10)
print(next(fib))
print(next(fib))
print(next(fib))

print("Hey")

#GUARANTEED EXAM QUESTION. Implement one of the itertools/ or any other function without using it.


