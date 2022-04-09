def capital_case(x):
    if x.isalpha():
        return x.upper()
    return x


def test_capital_case1():
    assert capital_case("*") == "*"
    assert capital_case("0") == "0"


def test_capital_case2():
    assert capital_case("a") == "A"
    assert capital_case("z") == "Z"
    assert capital_case("D") == "D"

