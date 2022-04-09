class Calculator():
    def add(self, x, y):
        return x + y


class TestCalculator():
    def test_Add(self):
        assert Calculator.add(2,3) == 5
        assert (Calculator.add("happy", "birthday") == "happybirthday")
        assert (Calculator.add(-2, 3) == 1)
