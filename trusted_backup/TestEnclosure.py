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
def tiger4():
    return Animal("tiger", "ti", 15)


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


def employee3():
    return Employee("employee3", "Paris")


def test_clean(enclosure1, enclosure2, zoo1):
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)

    enclosure2.clean()

    assert (len(enclosure1.cleaningRecord) == 1)
    assert (len(enclosure2.cleaningRecord) == 2)# In my implementation upon enclosure object is created it is already cleaned at the moment.

    assert (enclosure2.cleaningRecord[-1] == datetime.datetime.now())


def test_add_animal(zoo1, enclosure1, enclosure2, tiger1, tiger2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)

    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)

    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)


def test_remove_animal(zoo1, enclosure1, tiger1, tiger2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)

    zoo1.add_enclosure(enclosure1)

    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)

    enclosure1.remove_animal(tiger2)

    assert (len(enclosure1.animals) == 1)
    assert (enclosure1.animals[0] == tiger1)



def test_get_total_animals_per_species_in_enclosure(zoo1,enclosure1,tiger1,tiger2,tiger3,tiger4):

    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)
    zoo1.addAnimal(tiger4)

    zoo1.add_enclosure(enclosure1)

    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)
    enclosure1.add_animal(tiger3)
    enclosure1.add_animal(tiger4)

    mydict = enclosure1.get_total_animals_per_species_in_enclosure()

    assert (len(mydict) == 3)                       # Since we have only tiger1, and tiger4 are of the species name "tiger"

    xdict = {
    "tiger":2,
    "tiger2":1,
    "tiger3":1
    }

    assert (mydict == xdict)













