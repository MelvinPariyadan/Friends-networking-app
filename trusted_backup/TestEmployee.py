import datetime

import pytest

from animal import Animal
from zoo import Zoo
from enclosure import Enclosure
from care_taker import Employee


@pytest.fixture
def tiger1():
    return Animal("tiger", "ti", 12)


@pytest.fixture
def tiger2():
    return Animal("tiger2", "ti", 2)


@pytest.fixture
def tiger3():
    return Animal("tiger3", "xi", 10)


@pytest.fixture
def enclosure1():
    return Enclosure("enclosure1", 100)


@pytest.fixture
def enclosure2():
    return Enclosure("enclosure2", 50)


@pytest.fixture
def zoo1():
    return Zoo()


@pytest.fixture
def employee1():
    return Employee("employee1", "Chile")


@pytest.fixture
def employee2():
    return Employee("employee2", "Amsterdam")

@pytest.fixture
def employee3():
    return Employee("employee3", "Paris")



# def test_remove(zoo1,tiger1,tiger2,employee1,employee2):
#     zoo1.addAnimal(tiger1)
#     zoo1.addAnimal(tiger2)
#     zoo1.add_employee(employee1)
#     zoo1.add_employee(employee2)
#
#     employee1.add_animal(tiger1)
#     employee1.add_animal(tiger2)
#
#     employee1.remove(employee2,zoo1)
#
#     assert (employee1 not in zoo1.employees)
#     assert (len(employee2.animals) == 2)
#

def test_add_animal(zoo1, tiger1, tiger2, employee1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.add_employee(employee1)

    assert (tiger1 not in employee1.animals)
    employee1.add_animal(tiger1)
    employee1.add_animal(tiger2)



    assert(len(employee1.animals) == 2)
    assert(tiger1 in employee1.animals)
    assert (tiger2 in employee1.animals)





def test_remove_animal(zoo1,tiger1,tiger2,employee1,employee2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.add_employee(employee1)

    employee1.add_animal(tiger1)
    employee1.add_animal(tiger2)

    employee1.remove_animal(tiger2)

    assert(employee1.animals[0] == tiger1)
    assert(len(employee1.animals) == 1)


def test_get_number_of_animals(zoo1,tiger1,tiger2,employee1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.add_employee(employee1)

    employee1.add_animal(tiger1)
    employee1.add_animal(tiger2)

    assert(employee1.get_number_of_animals() == 2)





































