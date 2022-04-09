import uuid 
import datetime
# from zoo import *
class Animal: 
    def __init__ (self, species_name, common_name, age): 
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = [datetime.datetime.now()] # Every animal upon creation eats once. This implementation makes creating a feeding plan easier
        self.medical_record =[datetime.datetime.now()]
        self.enclosure = None 
        self.care_taker = None




        # add more as required here 
        
    # simply store the current system time when this method is called    
    def feed(self): 
        self.feeding_record.append(datetime.datetime.now())

    def medical_checkup(self):
        self.medical_record.append(datetime.datetime.now())

    def gives_birth(self):
        child = Animal(self.species_name,self.common_name,0)
        child.enclosure = self.enclosure

        return child



    def change_enclosure(self,enclosure_id):
        self.enclosure =enclosure_id


    def change_caretaker(self,employee_id):
        self.care_taker = employee_id









