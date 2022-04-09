from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder

from zoo import Zoo
from enclosure import Enclosure
from care_taker import Employee
from animal import Animal

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder
zooma_api = Api(zooma_app)

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True,
                           help='The scientific name of the animal, e,g. Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, help='The age of the animal, e.g., 12')


@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal(species, name, age)
        # add the animal to the zoo
        my_zoo.addAnimal(new_animal)
        return jsonify(new_animal)


@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
    def get(self, animal_id):
        search_result = my_zoo.getAnimal(animal_id)
        if not search_result:
            return jsonify(f"Animal with ID {animal_id} was not found")
        return jsonify(search_result)  # this is automatically jsonified by flask-restx

    def delete(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)

        #I added this code to your code to  keep the data correct across all entities

        employee = my_zoo.get_employee(targeted_animal.care_taker)
        enclosure = my_zoo.get_enclosure(targeted_animal.enclosure)

        if employee:
            employee.animals.remove(targeted_animal)
        if enclosure:
            enclosure.animals.remove(targeted_animal)

        return jsonify(f"Animal with ID {animal_id} was removed")


@zooma_api.route('/animals')
class AllAnimals(Resource):
    def get(self):
        return jsonify(my_zoo.animals)


@zooma_api.route('/animal/<animal_id>/feed')
class FeedAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)


@zooma_api.route("/animal/<animal_id>/vet")
class Medical_Checkup(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.medical_checkup()
        return jsonify(targeted_animal)


home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True)
@zooma_api.route("/animal/<animal_id>/home")
class Home_Assignment(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        args = home_parser.parse_args()

        enclosure_id = args['enclosure_id']
        targeted_animal = my_zoo.getAnimal(animal_id)

        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)


        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")


        old_enclosure = my_zoo.get_enclosure(targeted_animal.enclosure)


        if old_enclosure:
            old_enclosure.animals.remove(targeted_animal)

        targeted_animal.change_enclosure(enclosure_id)

        targeted_enclosure.animals.append(targeted_animal)

        return jsonify(targeted_animal)


birth_parser = reqparse.RequestParser()
birth_parser.add_argument('mother_id', type=str, required=True)
@zooma_api.route("/animal/birth/")
class Birth(Resource):
    @zooma_api.doc(parser=birth_parser)
    def post(self):
        args = birth_parser.parse_args()
        mother_id = args['mother_id']
        parent = my_zoo.getAnimal(mother_id)
        if not parent:
            return jsonify(f"Animal with ID {mother_id} was not found")

        child = parent.gives_birth()
        my_zoo.addAnimal(child)

        mother_enclosure = my_zoo.get_enclosure(parent.enclosure)
        if mother_enclosure:
            mother_enclosure.animals.append(child)

        return jsonify(child)


death_parser = reqparse.RequestParser()
death_parser.add_argument("animal_id", type=str, required=True)
@zooma_api.route("/animal/death/")
class Death(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        args = death_parser.parse_args()
        dead_animal_id = args['animal_id']

        targeted_animal = my_zoo.getAnimal(dead_animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {dead_animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)

        employee = my_zoo.get_employee(targeted_animal.care_taker)
        enclosure = my_zoo.get_enclosure(targeted_animal.enclosure)

        if employee:
            employee.animals.remove(targeted_animal)
        if enclosure:
            enclosure.animals.remove(targeted_animal)


        return jsonify(f"Animal with ID {dead_animal_id} was removed")


@zooma_api.route("/animals/stat/")
class Stat(Resource):
    # @zooma_api.doc(parser=stats_parser)
    def get(self):
        data = my_zoo.get_stats_animals()
        return jsonify(data)


enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True)
enclosure_parser.add_argument('space', type=int, required=True)
@zooma_api.route("/enclosure")
class AddEnclosure(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        args = enclosure_parser.parse_args()
        name = args['name']
        space = args['space']
        new_enclosure = Enclosure(name, space)

        my_zoo.add_enclosure(new_enclosure)
        return jsonify(new_enclosure)


@zooma_api.route("/enclosures")
class GetEnclosures(Resource):
    def get(self):
        return jsonify(my_zoo.enclosures)


@zooma_api.route("/enclosures/<enclosure_id>/clean")
class CleanEnclosure(Resource):
    def post(self, enclosure_id):
        enclosure = my_zoo.get_enclosure(enclosure_id)
        if not enclosure:
            return f"Enclosure with ID {enclosure_id} was not found"
        enclosure.clean()
        return jsonify(enclosure)


@zooma_api.route("/enclosures/<enclosure_id>/animals")
class AnimalDetailsEnclosure(Resource):
    def get(self, enclosure_id):
        enclosure = my_zoo.get_enclosure(enclosure_id)
        if not enclosure:
            return f"Enclosure with ID {enclosure_id} was not found"
        return jsonify(enclosure.animals)


@zooma_api.route("/enclosure/<enclosure_id>")
class DeleteEnclosure(Resource):
    def delete(self, enclosure_id):
        enclosure = my_zoo.get_enclosure(enclosure_id)
        if not enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")

        my_zoo.delete_enclosure(enclosure)

        return jsonify(f"Enclosure with ID {enclosure_id} was removed")


employee_parser = reqparse.RequestParser()
employee_parser.add_argument('name', type=str, required=True)
employee_parser.add_argument('address', type=str, required=True)
@zooma_api.route("/employee/")
class AddEmployee(Resource):
    @zooma_api.doc(parser=employee_parser)
    def post(self):
        args = employee_parser.parse_args()
        name = args['name']
        address = args['address']

        new_employee = Employee(name, address)
        my_zoo.add_employee(new_employee)

        return jsonify(new_employee)


@zooma_api.route("/employee/<employee_id>/care/<animal_id>/")
class EmployeeAssignedToAnimal(Resource):
    def post(self, employee_id, animal_id):
        animal = my_zoo.getAnimal(animal_id)

        if not animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        # If there was an old employee assigned to caretaker we remove it
        if animal.care_taker:
            old_employee = my_zoo.get_employee(animal.care_taker)
            if old_employee:
                old_employee.remove_animal(animal)

        new_employee = my_zoo.get_employee(employee_id)

        if not new_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")

        animal.change_caretaker(employee_id)

        new_employee.add_animal(animal)

        return jsonify(new_employee)


@zooma_api.route("/employee/<employee_id>/care/animals")
class EmployeesAnimals(Resource):
    def get(self, employee_id):
        employee = my_zoo.get_employee(employee_id)
        if not employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        return jsonify(employee.animals)


@zooma_api.route("/employees/")
class Employeess(Resource):
    def get(self):
        return jsonify(my_zoo.employees)


@zooma_api.route("/employees/stats")
class EmployeeStats(Resource):
    def get(self):
        data = my_zoo.get_stats_employees()
        return jsonify(data)


@zooma_api.route("/employee/<employee_id>")
class DeleteEmployee(Resource):
    def delete(self, employee_id):
        old_employee = my_zoo.get_employee(employee_id)
        if not old_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")

        new_care_taker = my_zoo.assign_new_care_taker(old_employee)

        if not new_care_taker:
            return jsonify(f"Zoo does not have any Employees added at the moment. (for the relevant animals) "
                           f"animal.care_taker = None")

        return jsonify(new_care_taker)


@zooma_api.route("/tasks/cleaning/")
class TaskCleaning(Resource):
    def get(self):
        my_zoo.create_cleaningPlan()
        return jsonify(my_zoo.cleaning_plan)


@zooma_api.route("/tasks/medical")
class TasksMedical(Resource):
    def get(self):
        my_zoo.create_medicalPlan()
        return jsonify(my_zoo.medical_plan)


@zooma_api.route("/tasks/feeding")
class TasksFeeding(Resource):
    def get(self):
        my_zoo.create_feedingPlan()
        return jsonify(my_zoo.feeding_plan)


if __name__ == '__main__':
    zooma_app.run(debug=False, port=7890)


# /HOME / STATS TEST IT IT DOES NOT WORK




