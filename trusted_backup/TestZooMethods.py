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
    return Animal("tiger3", "xi", 9)


@pytest.fixture
def tiger4():
    return Animal("tiger", "xi", 9)


@pytest.fixture
def donkey1():
    return Animal("donkey1", "dk", 5)


@pytest.fixture
def donkey2():
    return Animal("donkey2", "dk", 2)


@pytest.fixture
def donkey3():
    return Animal("donkey3", "dk", 3)


@pytest.fixture
def donkey4():
    return Animal("donkey1", "dk", 6)


@pytest.fixture
def enclosure1():
    return Enclosure("enclosure1", 100)


@pytest.fixture
def enclosure2():
    return Enclosure("enclosure2", 50)


@pytest.fixture
def enclosure3():
    return Enclosure("enclosure3", 50)


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


#####

def test_add_employee(zoo1, employee1, employee2):
    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)

    assert (len(zoo1.employees) == 2)
    assert (zoo1.employees[-1] == employee2)


def test_get_employee(zoo1, employee1, employee2):
    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)

    the_employee = zoo1.get_employee(employee2.employee_id)

    assert (the_employee == employee2)
    assert (the_employee != employee1)
    assert (len(zoo1.employees) == 2)

    wierd_input = zoo1.get_employee("*sldfjlkj")
    wierd_input2 = zoo1.get_employee(None)
    assert (wierd_input is None)
    assert (wierd_input2 is None)


def test_remove_employee(zoo1, employee1, employee2, employee3):
    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)
    zoo1.add_employee(employee3)

    zoo1.remove_employee(employee2.employee_id)

    assert (employee2 not in zoo1.employees)
    assert (len(zoo1.employees) == 2)


def test_addAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)

    assert (len(zoo1.animals) == 1)
    assert (zoo1.animals[0] == tiger1)


def test_removeAnimal(zoo1, tiger1, donkey1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(donkey1)

    zoo1.removeAnimal(tiger1)

    assert (len(zoo1.animals) == 1)
    assert (donkey1 in zoo1.animals)
    assert (tiger1 not in zoo1.animals)


def test_getAnimal(zoo1, tiger1, tiger2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)

    the_animal = zoo1.getAnimal(tiger2.animal_id)

    assert (the_animal == tiger2)
    assert (the_animal != tiger1)

    wierd_input = zoo1.getAnimal("*sldfjlkj")
    wierd_input2 = zoo1.getAnimal(None)
    assert (wierd_input is None)
    assert (wierd_input2 is None)


def test_add_enclosure(zoo1, enclosure1):
    zoo1.add_enclosure(enclosure1)

    assert (zoo1.enclosures[0] == enclosure1)
    assert (len(zoo1.enclosures) == 1)


def test_get_enclosure(zoo1, enclosure1, enclosure2):
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)

    the_enclosure = zoo1.get_enclosure(enclosure2.enclosure_id)

    assert (the_enclosure == enclosure2)
    assert (the_enclosure != enclosure1)

    wierd_input = zoo1.get_enclosure("*sldfjlkj")
    wierd_input2 = zoo1.get_enclosure(None)
    assert (wierd_input is None)
    assert (wierd_input2 is None)


########################################################################################
# Testing animal_stats functions and their sub functions here

# 1 and 4 of each animal are same species hence we should get 4 values
def test_get_total_animals_per_species(zoo1, enclosure1, tiger1, tiger2, tiger4, donkey1, donkey2, donkey4):
    mydict = zoo1.get_total_animals_per_species()

    assert (len(mydict) == 0)

    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger4)
    zoo1.addAnimal(donkey1)
    zoo1.addAnimal(donkey2)
    zoo1.addAnimal(donkey4)

    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(donkey4)

    mydict = zoo1.get_total_animals_per_species()

    assert (len(mydict) == 4)  # Since we have only tiger1, and tiger4 are of the species name "tiger"

    xdict = {
        "tiger": 2,
        "tiger2": 1,
        "donkey1": 2,
        "donkey2": 1
    }

    assert (mydict == xdict)


def test_avgAnimalsPerEnclosure(zoo1, enclosure1, enclosure2, tiger1, tiger2, tiger3, ):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    assert (zoo1.avgAnimalsPerEnclosure() is None)

    zoo1.add_enclosure(enclosure1)
    assert (zoo1.avgAnimalsPerEnclosure() == 3)
    zoo1.add_enclosure(enclosure2)
    assert (zoo1.avgAnimalsPerEnclosure() == 1.5)


def test_number_of_enclosures_with_multiple_species(zoo1, enclosure1, enclosure2, enclosure3, tiger1, tiger2, tiger4,
                                                    donkey1, donkey2, donkey4):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger4)

    zoo1.addAnimal(donkey1)
    zoo1.addAnimal(donkey2)
    zoo1.addAnimal(donkey4)

    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    zoo1.add_enclosure(enclosure3)

    # No multiple species
    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger4)
    # counts
    enclosure2.add_animal(tiger2)
    enclosure2.add_animal(donkey1)
    # counts as well as species name slightly different
    enclosure3.add_animal(donkey2)
    enclosure3.add_animal(donkey4)

    num_of_enclosures_with = zoo1.number_of_enclosures_with_multiple_species()
    assert (num_of_enclosures_with == 2)

    enclosure2.remove_animal(donkey1)
    num_of_enclosures_with = zoo1.number_of_enclosures_with_multiple_species()
    assert (num_of_enclosures_with == 1)


def test_get_space(zoo1, enclosure1):
    zoo1.add_enclosure(enclosure1)
    assert (zoo1.get_space(enclosure1) == 100)
    # There is no need to test this sub function for wierd input as end user cannot use this.
    # This is true for all the sub functions for each get_stats method


def test_get_number_of_animals(zoo1, enclosure1, enclosure2, tiger1, donkey1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(donkey1)

    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)

    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(donkey1)

    my_value_1 = zoo1.get_number_of_animals(enclosure1)
    my_value_2 = zoo1.get_number_of_animals(enclosure2)

    assert (my_value_1 == 2)
    assert (my_value_2 == 0)


def test_avg_space_per_animal_per_enclosure(zoo1, enclosure1, enclosure2, enclosure3, tiger1, tiger2, tiger3, donkey1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)
    zoo1.addAnimal(donkey1)

    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    zoo1.add_enclosure(enclosure3)

    # enclosure 1 space = 100
    # enclosure 2 space = 50

    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)
    enclosure1.add_animal(tiger3)

    # expected 100/3

    enclosure2.add_animal(donkey1)

    # expected 50/1

    # enclosure 3 expected : Not crash

    mydict = zoo1.avg_space_per_animal_per_enclosure()
    assert (len(mydict) == 3)
    xdict = {
        enclosure1.enclosure_id: 100 / 3,
        enclosure2.enclosure_id: 50 / 1,
        enclosure3.enclosure_id: None
    }

    assert (mydict == xdict)


def test_get_stats_animals(zoo1, tiger1, tiger2, tiger3, tiger4, donkey1, donkey2, donkey3, donkey4, enclosure1,
                           enclosure2, enclosure3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)
    zoo1.addAnimal(tiger4)

    zoo1.addAnimal(donkey1)
    zoo1.addAnimal(donkey2)
    zoo1.addAnimal(donkey3)
    zoo1.addAnimal(donkey4)

    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    zoo1.add_enclosure(enclosure3)

    enclosure1.add_animal(tiger1)
    enclosure1.add_animal(tiger2)
    enclosure1.add_animal(donkey2)

    enclosure2.add_animal(donkey4)
    enclosure2.add_animal(donkey1)

    enclosure3.add_animal(donkey3)
    enclosure3.add_animal(tiger3)
    enclosure3.add_animal(tiger4)

    mydict = zoo1.get_stats_animals()

    assert (len(mydict) == 4)
    # Each of these functions in xdict has already been tested above
    xdict = {
        "totalAnimalsPerSpecies": zoo1.get_total_animals_per_species(),
        "avgZoo": zoo1.avgAnimalsPerEnclosure(),
        "totalEnclosuresWithMultipleSpecies": zoo1.number_of_enclosures_with_multiple_species(),
        "avgSpacePerAnimal": zoo1.avg_space_per_animal_per_enclosure()

    }

    assert (mydict == xdict)
    assert (mydict[
                "totalEnclosuresWithMultipleSpecies"] == 2)  # 2 since enclosure 2 only has single species donkey1
    # and 4 are same species


########################################################################################

########################################################################################
# Testing employee_stats functions and their sub functions here

def test_get_max_stats(zoo1, employee1, employee2, employee3, tiger1, tiger2, tiger3, tiger4):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)
    zoo1.add_employee(employee3)

    employee2.add_animal(tiger1)
    employee3.add_animal(tiger2)
    employee3.add_animal(tiger3)

    the_max_length, the_employee = zoo1.get_max_stats()
    ############################################################################################ Still need to test the values

    assert (the_employee == employee3)
    assert (the_employee != employee1)

    employee2.add_animal(tiger4)
    the_max_length, the_employee = zoo1.get_max_stats()

    assert (
            the_employee == employee3)  # in my implementation if there are 2 employees with the largest amount of
    # animals. it takes the latter employee. Hence, should be true


def test_get_min_stats(zoo1, employee1, employee2, employee3, tiger1, tiger2, tiger3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)
    zoo1.add_employee(employee3)

    employee2.add_animal(tiger1)
    employee3.add_animal(tiger2)
    employee3.add_animal(tiger3)

    the_min_length, the_employee = zoo1.get_min_stats()
    ############################################################################################ Still need to test the values

    assert (the_employee == employee1)
    assert (the_employee != employee2)


def test_get_avg_stats(zoo1, employee1, employee2, tiger1, tiger2, tiger3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    # Does not crash when division by zero is attempted
    assert (zoo1.get_avg_stats() is None)

    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)

    assert (zoo1.get_avg_stats() is not None)

    assert (zoo1.get_avg_stats() == 3 / 2)


def test_get_stats_employees(zoo1, employee1, employee2, employee3, tiger1, tiger2, tiger3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)
    zoo1.add_employee(employee3)

    employee2.add_animal(tiger1)
    employee3.add_animal(tiger2)
    employee3.add_animal(tiger3)

    mydict = zoo1.get_stats_employees()
    assert (len(mydict) == 3)

    # These sub functions have been tested
    xdict = {
        "max_employee": 2,
        "min_employee": 0,
        "avg_employee": 1
    }

    assert (mydict == xdict)


def test_create_feedingPlan(zoo1, tiger1, tiger2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.create_feedingPlan()

    current_date = datetime.datetime.now()
    current_date = current_date + datetime.timedelta(days=2)  # next feeding date

    current_date_formatted = f"{current_date.day}:{current_date.month}:{current_date.year}"
    # I wanted to write the expected date as a string but the test would crash after today. Hence, I decided to use a
    # formatted variable that takes in today's date.

    xdict = {
        tiger1.animal_id: current_date_formatted,
        tiger2.animal_id: current_date_formatted
    }

    assert (zoo1.feeding_plan == xdict)

    tiger1.feed()
    tiger2.feed()
    zoo1.create_feedingPlan()

    xdict = {
        tiger1.animal_id: current_date_formatted,
        tiger2.animal_id: current_date_formatted
    }
    assert (zoo1.feeding_plan == xdict)


def test_create_medicalPlan(zoo1, tiger1, tiger2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.create_medicalPlan()

    current_date = datetime.datetime.now()
    current_date = current_date + datetime.timedelta(days=35)  # next feeding date

    current_date_formatted = f"{current_date.day}:{current_date.month}:{current_date.year}"
    # I wanted to write the expected date as a string but the test would crash after today. Hence, I decided to use a
    # formatted variable that takes in today's date.

    xdict = {
        tiger1.animal_id: current_date_formatted,
        tiger2.animal_id: current_date_formatted
    }

    assert (zoo1.medical_plan == xdict)

    tiger1.medical_checkup()
    tiger2.medical_checkup()
    zoo1.create_medicalPlan()

    xdict = {
        tiger1.animal_id: current_date_formatted,
        tiger2.animal_id: current_date_formatted
    }
    assert (zoo1.medical_plan == xdict)


# def test_assign_new_care_taker()


def test_create_cleaningPlan(zoo1, enclosure1, enclosure2):
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    zoo1.create_cleaningPlan()

    current_date = datetime.datetime.now()
    current_date = current_date + datetime.timedelta(days=3)  # next feeding date

    current_date_formatted = f"{current_date.day}:{current_date.month}:{current_date.year}"
    # I wanted to write the expected date as a string but the test would crash after today. Hence, I decided to use a
    # formatted variable that takes in today's date.

    xdict = {
        enclosure1.enclosure_id: current_date_formatted,
        enclosure2.enclosure_id: current_date_formatted
    }

    assert (len(zoo1.cleaning_plan) == 2)
    assert (zoo1.cleaning_plan == xdict)

    enclosure1.clean()
    enclosure2.clean()
    zoo1.create_cleaningPlan()

    xdict = {
        enclosure1.enclosure_id: current_date_formatted,
        enclosure2.enclosure_id: current_date_formatted
    }
    assert (zoo1.cleaning_plan == xdict)
    assert (len(zoo1.cleaning_plan) == 2)


def test_assign_new_care_taker(zoo1, employee1, employee2, tiger1, tiger2, tiger3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    zoo1.add_employee(employee1)
    zoo1.add_employee(employee2)

    employee1.add_animal(tiger1)
    employee2.add_animal(tiger2)
    employee2.add_animal(tiger3)

    zoo1.assign_new_care_taker(employee2)

    assert (tiger2 in employee1.animals)
    assert (tiger3 in employee1.animals)

    assert (employee2 not in zoo1.employees)


def test_delete_enclosure(zoo1, enclosure1, enclosure2, enclosure3, tiger1, tiger2, tiger3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    zoo1.add_enclosure(enclosure3)

    enclosure1.add_animal(tiger1)
    enclosure2.add_animal(tiger2)
    enclosure2.add_animal(tiger3)

    zoo1.delete_enclosure(enclosure1)
    zoo1.delete_enclosure(enclosure3)

    assert (len(zoo1.enclosures) == 1)
    assert (enclosure2 in zoo1.enclosures)
    assert (enclosure1 not in zoo1.enclosures)
    assert (enclosure3 not in zoo1.enclosures)

    assert (len(enclosure2.animals) == 3)
