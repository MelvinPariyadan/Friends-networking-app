def print_in_a_box(x):
    boxchar = "+"
    def myprint():
        print (boxchar*len(x)*2)
        print ("| "+x + " |")
        print(boxchar * len(x)*2)
    return myprint
f = print_in_a_box("Happy")
f()


print (f.__closure__[1].cell_contents)

print("************************************************************")

def sayhello():
    return("hello ")
def callme(f):
    print(f() + "and bye")
callme(sayhello)

print("************************************************************")

def nestedparent(f):
    def nested_child():
        print("before hello")
        f()
        print("after hello")
    return nested_child

@nestedparent
#hello = nestedparent(hello) implicitly. We are redefining hello
def hello():
    return "hello"


print(hello())
hello = nestedparent(hello)
print(hello())



print("######################################")


def mydecorator(f):
    def inner(name):
        print(f(name))
    return inner
@mydecorator
def hello(name):
    return "hello" + name
print(hello("Markus"))
