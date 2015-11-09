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
    #clues.append({"position": "2","drink": "milk"})
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
    """ Extract individual elements from the given clue list.
    Ie. all house colors, all drinks, all nationalities, etc. """
    elements = dict()
    for clue in clues:
        for key, value in clue.items():
            if key not in elements:
                elements[key] = [value]
            else:
                if value not in elements[key]:
                    elements[key].append(value)

    return elements

def check_houses(houses, clue):
    """ Check how many houses clue1 <-> clue2 could describe.
    Return number of houses, as well as the index of the last house matched. """
    possible_placements = 0
    possible_house = None

    print("Checking houses for clue: " + str(clue))

    for index, house in enumerate(houses):
        key1 = list(clue.keys())[0]  # eg. "person"
        key2 = list(clue.keys())[1]  # eg. "color"
        if (house.data[key1] == clue[key1] and house.data[key2] is None):
            # if house["person"] = "english" then house["color"] = "red"
            house.data[key2] = clue[key2] 
            possible_house = index
            possible_placements += 1 
        elif (house.data[key2] == clue[key2] and house.data[key1] is None):
            # if house["color"] = "red" then house["person"] = "english"
            house.data[key1] = clue[key1]
            possible_house = index
            possible_placements += 1 

    #print("possibilities for " + str(clue) + " are " + str(possible_placements))
    return possible_placements, possible_house





def main():
    """ Solve riddle. """
    house_number = 5
    houses = list()
    for index, house in enumerate(range(house_number)):
        houses.append(Household(index))

    assertions = build_assertions()

    assertion_used = [False] * len(assertions)
    # print("assertion_used: " + str(assertion_used))
    #assertions_cp = list(assertions)
    #compound_assertions = list()
    pos_p = re.compile(".*\[(.*):(.*)\]")  # position pattern
    elements = build_element_list(assertions)

    for clue_i, clue in enumerate(assertions):    
        if len(clue) == 2:
            if "position" not in clue.keys():
                possible_placements, possible_house = check_houses(houses, clue)
                if possible_placements == 1:  # guaranteed fit, one way or another
                    assertion_used[clue_i] = True
                    if houses[possible_house].data[key1] == clue[key1]:
                         # if house["person"] = "english" then house["color"] = "red"
                        houses[possible_house].data[key2] = clue[key2]
                    else:  # houses[possible_house].data[key2] == clue[key2]
                        # if house["color"] = "red" then house["person"] = "english"
                        houses[possible_house].data[key1] = clue[key1]

            else:  # position in clue
                position = clue["position"] # key1 is "position"
                key2 = list(clue.keys())  # get other key
                key2.remove("position")  
                key2 = key2[0]
                print("\n\nkey2 is: " + key2 + ", position: " + position)
                pos_data = re.match(pos_p, position)  # group(1) = "color", group(2) = "ivory"

                if pos_data is None:  # no pattern match
                    if position.isdigit() and int(position) < house_number:
                        possible_placements, possible_house = check_houses(houses, clue)
                        print("poss_pl: " + str(possible_placements) + ", poss_h: " + str(possible_house))
                        print("for clue: " + str(clue))
                        if possible_placements == 1:  # guaranteed fit, one way or another
                            assertion_used[clue_i] = True
                            if houses[possible_house].data["position"] == clue["position"]:
                                 # if house["person"] = "english" then house["color"] = "red"
                                houses[possible_house].data[key2] = clue[key2]
                            else:  # houses[possible_house].data[key2] == clue[key2]
                                # if house["color"] = "red" then house["person"] = "english"
                                houses[possible_house].data["position"] = clue["position"]

                    else:
                        print("Clue contains invalid position: " + position + ". Exiting...")
                        exit()

                else:  # pattern matched
                    comp_key = pos_data.group(1)  # comparison key: color
                    comp_val = pos_data.group(2)  # comparison value: ivory

                    if "right" in position:  
                        print("placeholder: position with right")
                        # clue 05: {"color": "green", "position": "right [color:ivory]"}

                        for i, h in enumerate(houses):
                            if h.data[comp_key] == comp_val:  # if color = ivory
                                pass

                    elif "left" in position:
                        print("placeholder: position with left")
                    elif "next" in position:
                        print("placeholder: position with next")
                        # clue 11: {"smoke": "kools", "position": "next [pet:horse]"}
                    else:
                        print("Clue contains invalid position modifier: " + position + ". Exiting...")
                        exit()

                    
                    
    #for e in elements:
        #print(e + ":    \t" + str(elements[e]) + "\n")
    print("House ##,\tcolor,\tresident,\tpet,\tdrink,\tsmoke")
    for house in houses:
        house.describe()
    print("Assertions used:\n" + str(assertion_used))










if __name__ == '__main__':
    main()
