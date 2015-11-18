#!/usr/bin/env python
from Household import Household

class ProblemData():
    """ A class aggregating the data pertaining to a particular Zebra puzzle.
    This includes a list with houses, the clues supplied, as well as various secondary structures. """
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
                        elements[key][value] = list(range(5))

        return elements

    def clean_elements(self):
        """ Check if a certain element now has a definite position, but is still
        listed as a possibility elsewhere. If so, remove that listing. 
        Return True if any changes are made, False otherwise. """
        progress = False
        for attr in self.elements:
            for e in self.elements[attr]:
                if len(self.elements[attr][e]) == 1:
                    certain = self.elements[attr][e][0]
                    for each in self.elements[attr]:
                        if certain in self.elements[attr][each]:
                            self.elements[attr][each].remove(certain)
                            progress = True     
                    self.elements[attr][e].append(certain)
                    self.houses[certain].data[attr] = e

            counting_list = [item for sublist in self.elements[attr].values() for item in sublist]
            #if attr == "color" : print(counting_list)
            for i in range(self.house_number):
                count = counting_list.count(i)
                if count == 1:
                    #print("count for sublist for " + attr + "=" + str(i) + " is: " + str(count))
                    # meaning there is only one possible position for this element
                    # check if this is news:
                    for single_element in self.elements[attr]:
                        if i in self.elements[attr][single_element]:
                            # got the element
                            if not self.houses[i].data[attr] == single_element:
                                self.houses[i].data[attr] = single_element
                                progress = True
                                self.elements[attr][single_element] = [i]
                                print("elimination got: " + single_element)
                        


        return progress

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
                for atb in self.elements[attribute]:
                    print("\t" + atb + "@" + str(self.elements[attribute][atb]))
                print("")         