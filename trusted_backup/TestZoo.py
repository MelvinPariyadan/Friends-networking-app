import pytest
import requests
import json

from animal import Animal


@pytest.fixture
def baseURL():
    return "http://127.0.0.1:7890"


@pytest.fixture
def tiger1():
    return Animal("tiger mum", "btiger1", 21)


@pytest.fixture
def tiger2():
    return Animal("tiger child", "btiger2", 2)


@pytest.fixture
def post_tiger1(baseURL, tiger1):
    tiger1_data = {"species": tiger1.species_name, "name": tiger1.common_name, "age": tiger1.age}
    return requests.post(baseURL + "/animal", data=tiger1_data)


class Testzoo():

    def test_one(self, baseURL, post_tiger1):
        x = requests.get(baseURL + "/animals")
        js = x.content
        animals = json.loads(js)

        assert (len(animals) == 1)
    #
    def test_two(self,baseURL,post_tiger1):
        x = requests.get(baseURL + "/animal/e26052df-52f5-4347-8cc1-243cf7713526")
        js = x.content
        data = json.loads(js)

        # assert (data == None)

        assert (data["species_name"] == tiger1.species_name)



