from main import *

class TestClass():
    def test_one(self):
        x = "hello"
        assert 'h' in x
    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')

    def test_three():
        assert Calculator.add(3,5) == 8