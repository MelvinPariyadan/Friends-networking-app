
def bold(f):
    def inner():
        x = "<b>" + f() + "<b>"
        return x
    return inner




def italic(f):
    def inner():
        x = "<i>" + f() + "<i>"
        return x
    return inner



def underline(f):
    def inner():
        x = "<u>" + f() + "<u>"
        return x
    return inner


@bold
@italic
@underline
def mp():
    return "hello world"

print(mp())