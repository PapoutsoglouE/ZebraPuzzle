#!/usr/bin/env python
from Household import Household
import re


def build_assertions():
    """ Construct and return a list including all statements 
    provided by the riddle itself. """
    clues = list()
    # each list element is a dictionary with 1 or 2 keys
    clues.append({"person": "english", "color": "red"})                     # 01
    clues.append({"person": "spanish", "pet": "dog"})                       # 02
    clues.append({"drink": "coffee", "color": "green"})                     # 03
    clues.append({"person": "ukrainian", "drink": "tea"})                   # 04
    clues.append({"color": "green", "position": "right [color:ivory]"})     # 05
    clues.append({"color": "ivory"})
    clues.append({"smoke": "old gold", "pet": "snails"})                    # 06
    clues.append({"smoke": "kools", "color": "yellow"})                     # 07
    clues.append({"drink": "milk", "position": "2"})                        # 08
    clues.append({"person": "norwegian", "position": "0"})                  # 09
    clues.append({"smoke": "chesterfields", "position": "next [pet:fox]"})  # 10
    clues.append({"pet": "fox"})
    clues.append({"smoke": "kools", "position": "next [pet:horse]"})        # 11
    clues.append({"pet": "horse"})
    clues.append({"smoke": "lucky strike", "drink": "orange juice"})        # 12 
    clues.append({"person": "japanese", "smoke": "parliaments"})            # 13
    clues.append({"person": "norwegian", "position": "next [color:blue]"})  # 14
    clues.append({"drink": "water"})
    clues.append({"pet": "zebra"})
    return clues

def build_element_list(clues):
    elements = dict()
    for clue in clues:
        for key, value in clue.items():
            if key not in elements:
                elements[key] = [value]
            else:
                if value not in elements[key]:
                    elements[key].append(value)

    return elements

def main():
    houseNumber = 5
    houses = list()
    for index, house in enumerate(range(houseNumber)):
        houses.append(Household(str(index)))

    assertions = build_assertions()

    assertion_used = [False] * len(assertions)
    print("assertion_used: " + str(assertion_used))
    assertions_cp = list(assertions)
    compound_assertions = list()
    pos_p = re.compile(".*\[(.*):(.*)\]")  # position pattern
    elements = build_element_list(assertions)

    for clue in assertions:    
        possible_placements = 5
        possible_house = None
        if len(clue) == 2:
            if "position" not in clue.keys():
                for index, house in enumerate(houses):
                    key1 = list(clue.keys())[0]  # eg. "person"
                    key2 = list(clue.keys())[1]  # eg. "color"
                    if house.data[key1] == clue[key1]:  # if house["person"] = "english"
                        house.data[key2] = clue[key2]   # then house["color"] = "red"
                        possible_house = index
                    elif house.data[key2] == clue[key2]:  # if house["color"] = "red"
                        house.data[key1] = clue[key1]     # then house["person"] = "english"
                        possible_house = index
                    else:  # neither clue matches 
                        possible_placements -= 1
                    print("possibilities for clue: " + str(clue) + " are: " + str(possible_placements))
                else:
                    if possible_placements == 1:
                        if houses[possible_placements].data[key1] == clue[key1]:  # if house["person"] = "english"
                            houses[possible_placements].data[key2] = clue[key2]   # then house["color"] = "red"
                        elif houses[possible_placements].data[key2] == clue[key2]:  # if house["color"] = "red"
                            houses[possible_placements].data[key1] = clue[key1]     # then house["person"] = "english"
            else:  # position in clue
                position = clue["position"]
                # get other key
                keys = list(clue.keys())
                keys.remove("position")
                key2 = keys[0]
                print("key2 is: " + key2 + ", position: " + position)
                if "right" in position:  
                    print("placeholder: position with right")
                    # clue 05: {"color": "green", "position": "right [color:ivory]"}
                    res = re.match(pos_p, position)
                    comp_key = res.group(1)  # comparison key: color
                    comp_val = res.group(2)  # comparison value: ivory
                    for i, h in enumerate(houses):
                        if h.data[comp_key] == comp_val:
                            pass

                elif "left" in position:
                    print("placeholder: position with left")
                elif "next" in position:
                    print("placeholder: position with next")
                    # clue 11: {"smoke": "kools", "position": "next [pet:horse]"}
                elif position.isdigit():
                    print("placeholder: position with digit")
                else:
                    print("Clue contains invalid position: " + position + ". Exiting...")
                    exit()
                    
                    
    #for e in elements:
        #print(e + ":    \t" + str(elements[e]) + "\n")
    for house in houses:
        house.describe()










if __name__ == '__main__':
    main()
