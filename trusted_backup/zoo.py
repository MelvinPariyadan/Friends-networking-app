import datetime
import random


class Zoo:
    def __init__(self):
        self.animals = []
        self.enclosures = []
        self.employees = []
        self.feeding_plan = {}
        self.medical_plan = {}
        self.cleaning_plan = {}


    ################################################################### Sub functions for get_employee_stats
    def get_max_stats(self):
        largest = 0
        max_employee = None

        for employee in self.employees:
            if employee.get_number_of_animals() >= largest:
                largest = employee.get_number_of_animals()
                max_employee = employee
        return len(max_employee.animals),max_employee

    def get_min_stats(self):
        smallest = len(self.animals)
        min_employee = None

        for employee in self.employees:
            if employee.get_number_of_animals() <= smallest:
                smallest = employee.get_number_of_animals()
                min_employee = employee
        return len(min_employee.animals),min_employee
    #Here I i am purposefully sending the min employee object as well in return. Later when an employee is removed. I will use this func to get the employee -> He will get the animals assigned


    def get_avg_stats(self):
        if len(self.employees) > 0:
            return len(self.animals) / len(self.employees)
        #default return in python is None

    ######################################################################

    def get_stats_employees(self):
        result = {}
        length_max,employee_max = self.get_max_stats()
        length_min,employee_min = self.get_min_stats()

        result["max_employee"] = length_max
        result["min_employee"] = length_min
        result["avg_employee"] = self.get_avg_stats()

        return result

    #######################################################################

    def add_employee(self, employee):
        self.employees.append(employee)

    def get_employee(self, employee_id):
        if employee_id:
            for employee in self.employees:
                if employee.employee_id == employee_id:
                    return employee

    def remove_employee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                self.employees.remove(employee)

    def addAnimal(self, animal):
        self.animals.append(animal)

    def removeAnimal(self, animal):
        self.animals.remove(animal)

    def getAnimal(self, animal_id):
        if animal_id:
            for animal in self.animals:
                if animal.animal_id == animal_id:
                    return animal

    def add_enclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def get_enclosure(self, enclosure_id):
        if enclosure_id:
            for enclosure in self.enclosures:
                if enclosure.enclosure_id == enclosure_id:
                    return enclosure


    ############################### Here are sub functions to make get_stats_animals function work

    def get_total_animals_per_species(self):
        totalAnimalsPerSpecies = {}
        for animal in self.animals:
            if animal.species_name not in totalAnimalsPerSpecies:
                totalAnimalsPerSpecies[animal.species_name] = 0
            totalAnimalsPerSpecies[animal.species_name] += 1

        return totalAnimalsPerSpecies

    def avgAnimalsPerEnclosure(self):
        if len(self.enclosures) > 0:
            return len(self.animals) / len(self.enclosures)


    ##@################################################################################
    def number_of_enclosures_with_multiple_species(self):
        count = 0
        for enclosure in self.enclosures:
            mydict = enclosure.get_total_animals_per_species_in_enclosure()
            if len(mydict) > 1:
                count += 1
        return count



    def get_space(self, enclosure):
        if enclosure:
            return enclosure.space

    def get_number_of_animals(self, enclosure):
        if enclosure:
            return len(enclosure.animals)



    def avg_space_per_animal_per_enclosure(self):
        data = {}
        for enclosure in self.enclosures:
            if len(enclosure.animals) > 0:
                data[enclosure.enclosure_id] = self.get_space(enclosure) / self.get_number_of_animals(enclosure)
            else:
                data[enclosure.enclosure_id] = None

        return data

    ####################################################################

    def get_stats_animals(self):
        result = {}

        result["totalAnimalsPerSpecies"] = self.get_total_animals_per_species()

        result["avgZoo"] = self.avgAnimalsPerEnclosure()

        result["totalEnclosuresWithMultipleSpecies"] = self.number_of_enclosures_with_multiple_species()

        result["avgSpacePerAnimal"] = self.avg_space_per_animal_per_enclosure()

        return result



    def create_feedingPlan(self):
        for animal in self.animals:
            time = animal.feeding_record[-1] + datetime.timedelta(days=2)
            time_formatted = f"{time.day}:{time.month}:{time.year}"
            self.feeding_plan[animal.animal_id] = time_formatted

    def create_medicalPlan(self):
        for animal in self.animals:
            time = animal.medical_record[-1] + datetime.timedelta(days=35)
            time_formatted = f"{time.day}:{time.month}:{time.year}"
            self.medical_plan[animal.animal_id] = time_formatted

    def create_cleaningPlan(self):
        for enclosure in self.enclosures:
            time = enclosure.cleaningRecord[-1] + datetime.timedelta(days=3)
            time_formatted = f"{time.day}:{time.month}:{time.year}"
            self.cleaning_plan[enclosure.enclosure_id] = time_formatted

    def assign_new_care_taker(self, old_employee):
        animals = old_employee.animals[::]
        self.remove_employee(old_employee.employee_id)
        if len(self.employees) > 0:
            length, new_care_taker = self.get_min_stats()  # Take the employee that has the least animals.
            for animal in animals:
                animal.change_caretaker(new_care_taker.employee_id)
            new_care_taker.animals.extend(animals)
            return new_care_taker
        else:
            for animal in animals:
                animal.care_taker = None

    def delete_enclosure(self, enclosure):
        animals = enclosure.animals
        self.enclosures.remove(enclosure)
        if len(self.enclosures) > 0:
            new_enclosure = random.choice(self.enclosures)
            new_enclosure.animals.extend(enclosure.animals)

            for animal in animals:
                animal.enclosure = new_enclosure.enclosure_id

        else:
            # There are no enclosures in the Zoo
            for animal in animals:
                animal.enclosure = None






