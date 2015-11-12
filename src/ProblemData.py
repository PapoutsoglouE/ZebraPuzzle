#!/usr/bin/env python
from Household import Household

class ProblemData():
    def __init__(self, house_number, assertions):
        self.house_number = house_number
        self.assertions = assertions
        self.assertions_used = [(True if len(x) < 2 else False) for x in assertions]
        self.houses = [Household(i) for i in range(house_number)]
        self.elements = self.build_element_list()


    def build_element_list(self):
        """ Extract individual elements from the given clue list.
        Ie. all house colors, all drinks, all nationalities, etc. 
        The produced structure follows the format: dict(dict(list)))
        eg. elements["pet"]["dog"] = [1,2,4], where [1,2,4] are the
        possible placements for the ["pet"]["dog"]. """
        elements = dict()
        for clue in self.assertions:
            for key, value in clue.items():
                if key not in elements:
                    elements[key] = dict()
                    elements[key][value] = list(range(5))
                else:
                    if value not in elements[key]:
                        elements[key][value] =  list(range(5))

        return elements


    def house_state(self):
        """ Print all houses with their current state. """
        print("House ##,\tcolor,\tresident,\tpet,\tdrink,\tsmoke")
        for house in self.houses:
            house.describe()        
        print()


    def element_state(self):
        """ Print all elements, and the possible positions for each. """
        for attribute in self.elements:
            if not attribute == "position":
                print(attribute + ":")
                for a in self.elements[attribute]:
                    print("\t" + a + "@" + str(self.elements[attribute][a]))
                print()         