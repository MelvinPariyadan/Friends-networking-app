import uuid
import datetime
class Enclosure:

    def __init__(self,name,space):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.space = space
        self.animals = []
        self.cleaningRecord = [datetime.datetime.now()] # Every Enclosure is cleaned upon creation. This implementation makes creating a cleaning plan easier
    def clean(self):
        self.cleaningRecord.append(datetime.datetime.now())

    def add_animal(self,animal):
        self.animals.append(animal)

    def remove_animal(self,animal):
        self.animals.remove(animal)


#################################################################################################
#I used the same function as from zoo but changed it for enclosure
    def get_total_animals_per_species_in_enclosure(self):
        totalAnimalsPerSpecies = {}
        for animal in self.animals:
            if animal.species_name not in totalAnimalsPerSpecies:
                totalAnimalsPerSpecies[animal.species_name] = 0
            totalAnimalsPerSpecies[animal.species_name] += 1

        return totalAnimalsPerSpecies




