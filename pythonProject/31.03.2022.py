try:
    x = int(input("enter a number"))
    print (1/0)

except (ArithmeticError,ValueError) as e:
    print("division by zero is not possible")
    print(e.__doc__)
except ValueError:
    print("can't convert to int")

finally:
    print("finally here")

print("hi")