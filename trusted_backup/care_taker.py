import uuid
class Employee:
    def __init__(self,name,address):
        self.employee_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals = []

    def remove_animal(self,animal):
        self.animals.remove(animal)

    def add_animal(self,animal):
        self.animals.append(animal)
    def get_number_of_animals(self):
        return len(self.animals)



