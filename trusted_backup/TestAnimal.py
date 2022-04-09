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


def test_addingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    assert (tiger1 in zoo1.animals)
    zoo1.addAnimal(tiger2)

    assert (len(zoo1.animals) == 2)


def test_feedingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    tiger1.feed()
    assert (len(tiger1.feeding_record) == 2) # In my implementation upon animal object is created it is already fed at the moment.
    assert (tiger1.feeding_record[-1] == datetime.datetime.now())




def test_medical_checkup(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    tiger1.medical_checkup()
    assert (len(tiger1.medical_record) == 2) # In my implementation upon animal object is created it is already vet at the moment.
    assert (tiger1.medical_record[-1] == datetime.datetime.now())



def test_gives_birth(zoo1, tiger1, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.add_enclosure(enclosure1)
    tiger1.change_enclosure(enclosure1.enclosure_id)
    enclosure1.add_animal(tiger1)

    tiger1_child = tiger1.gives_birth()
    assert (len(zoo1.animals) == 1) # the reason is because the child is added to zoo through the zooma app. This avoids needing to pass my_zoo as parameter
    assert (len(enclosure1.animals) == 1) #Same reason as above
    assert (tiger1_child.enclosure == tiger1.enclosure)
    assert (tiger1_child.age == 0)
    assert (tiger1_child.species_name == "tiger")
    assert (tiger1_child.common_name == "ti")






def test_change_enclosure(zoo1,enclosure1,tiger1):
    zoo1.addAnimal(tiger1)
    zoo1.add_enclosure(enclosure1)

    enclosure1.add_animal(tiger1)

    assert (tiger1.enclosure == None)

    tiger1.change_enclosure(enclosure1.enclosure_id)

    assert(tiger1.enclosure == enclosure1.enclosure_id)

def test_change_caretaker(zoo1,tiger1,tiger2,employee1,employee2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)

    #tiger 1 already has an employee
    tiger1.care_taker = employee1.employee_id

    tiger1.change_caretaker(employee2.employee_id)
    assert (tiger1.care_taker == employee2.employee_id)

    #tiger 2 self.care_taker is still the default None
    tiger2.change_caretaker(employee2.employee_id)
    assert (tiger1.care_taker == employee2.employee_id)

























