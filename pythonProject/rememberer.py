import time

def parent(f):

    def inner():
        f()
    return inner


@parent
def m1 ():
    return time.time()
print (m1())
print (m1())
time.sleep(2)
print (m1())
print (m1())


print("########....................###############....................##############")



def remember(f):
    def nested():
        x = f()
        return x
    return nested
@remember
def m1(): # m1 = remember(m1)
    return time.time()


print (m1())
print (m1())
time.sleep(2)
print (m1())
print (m1())




