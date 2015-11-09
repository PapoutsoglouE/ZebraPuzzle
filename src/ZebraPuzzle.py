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
    possible_fits = 0
    fit_index = None
    # print("Checking houses for clue: " + str(clue))

    for index, house in enumerate(houses):
        key1, key2 = list(clue.keys())  # eg. "person", "color"
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
        elif (house.data[key1] is None and house.data[key2] is None):
            fit_index = index
            possible_fits += 1 

    # print("possibilities for " + str(clue) + " are " + str(possible_placements)
    #       + " and fits: " + str(possible_fits))
    return possible_placements, possible_house, possible_fits, fit_index


def main():
    """ Solve riddle. """
    house_number = 5
    houses = list()
    for index, house in enumerate(range(house_number)):
        houses.append(Household(index))

    assertions = build_assertions()
    assertion_used = list(map(lambda x: True if len(x)<2 else False, assertions))
    #assertions_cp = list(assertions)
    #compound_assertions = list()
    pos_p = re.compile(".*\[(.*):(.*)\]")  # position pattern
    elements = build_element_list(assertions)

    for round in range(2):
        progress_made = False  # have any changes (progress) been made this round?
        for clue_i, clue in enumerate(assertions):    
            if len(clue) == 2 and not assertion_used[clue_i]:
                key1, key2 = list(clue.keys())  # eg. "person", "color"
                if "position" not in clue.keys():
                    possible_placements, possible_house, fits, fit_index = check_houses(houses, clue)
                    if possible_placements == 1:  # guaranteed fit, one way or another
                        progress_made = True
                        assertion_used[clue_i] = True
                        if houses[possible_house].data[key1] == clue[key1]:
                             # if house["person"] = "english" then house["color"] = "red"
                            houses[possible_house].data[key2] = clue[key2]
                        else:  # houses[possible_house].data[key2] == clue[key2]
                            # if house["color"] = "red" then house["person"] = "english"
                            houses[possible_house].data[key1] = clue[key1]
                    elif possible_placements == 0 and fits == 1:
                        progress_made = True
                        houses[fit_index].data[key1] = clue[key1]
                        houses[fit_index].data[key2] = clue[key2]

                    elif fits == 0:
                        print("Cannot possibly fit clue: " + str(clue) + ". Exiting.")
                        # print("House ##,\tcolor,\tresident,\tpet,\tdrink,\tsmoke")
                        # for house in houses:
                        #     house.describe()    
                        exit()
                        # TODO: handle this possibility better for potential future loop-over

                else:  # position in clue
                    position = clue["position"] # key1 is "position"
                    key2 = key2 if key1 == "position" else key2 # get other key
                    print("\n\nkey2 is: " + key2 + ", position: " + position)
                    pos_data = re.match(pos_p, position)  # group(1) = "color", group(2) = "ivory"

                    if pos_data is None:  # no pattern match
                        if position.isdigit() and int(position) < house_number:
                            possible_placements, possible_house, fits, fit_index = check_houses(houses, clue)
                            print("poss_pl: " + str(possible_placements) + ", poss_h: " + str(possible_house))
                            print("for clue: " + str(clue))
                            if possible_placements == 1:  # guaranteed fit, one way or another
                                progress_made = True
                                assertion_used[clue_i] = True
                                if houses[possible_house].data["position"] == clue["position"]:
                                     # if house["person"] = "english" then house["color"] = "red"
                                    houses[possible_house].data[key2] = clue[key2]
                                else:  # houses[possible_house].data[key2] == clue[key2]
                                    # if house["color"] = "red" then house["person"] = "english"
                                    houses[possible_house].data["position"] = clue["position"]

                            elif possible_placements == 0 and fits == 1:
                                progress_made = True
                                houses[fit_index].data[key1] = clue[key1]
                                houses[fit_index].data[key2] = clue[key2]
                            elif fits == 0:
                                print("Cannot possibly fit clue: " + str(clue) + ". Exiting.")
                                # print("House ##,\tcolor,\tresident,\tpet,\tdrink,\tsmoke")
                                # for house in houses:
                                #     house.describe()    
                                exit()
                                # TODO: handle this possibility better for potential future loop-over

                        else:
                            print("Clue contains invalid position: " + position + ". Exiting...")
                            exit()
                            # TODO: handle possibility of clue appearing invalid pointing to error in logic

                    else:  # pattern matched
                        comp_key, comp_val = pos_data.groups()  # comparison key: color, comparison value: ivory
                        # clue[key2] = green, key2 = color
                        # comp_key = color, comp_val = ivory
                        # TODO: toggle progress_made = True
                        comp_index = None  # index of house with color = ivory
                        comp2_index = None # index of house with color = green
                        # example: {"color": "green", "position": "right [color:ivory]"}
                        for i, h in enumerate(houses):
                            if h.data[comp_key] == comp_val:  # if color = ivory
                                comp_index = i
                            elif h.data[key2] == clue[key2]:  # if color = green
                                comp2_index = i

                        #side_match = f(houses, assertions, assertion_used, clue_i,
                                       #comp_key, comp_val, comp_index, comp2_index, key2)
                        if "right" in position:  
                            print("placeholder: position with right")
                            
                            if comp_index is not None and comp_index + 1 < house_number :
                                # comp_index points to the house where the [color:ivory] condition is fulfilled 
                                if houses[comp_index + 1].data[key2] is None:
                                    # if the house to the right of the house with [color:ivory] has no
                                    # color assigned, its color will be green
                                    assertions.append({key2: clue[key2], "position": str(comp_index + 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True
                            elif comp2_index is not None and comp2_index - 1 >= 0:
                                # comp2_index points to the house where the {color:green} condition is fulfilled 
                                if houses[comp2_index - 1].data[comp_key] is None:
                                    assertions.append({comp_key: comp_val, "position": str(comp2_index - 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True                       


                        elif "left" in position:
                            print("placeholder: position with left")
                            if comp2_index is not None and comp2_index + 1 < house_number:
                                # comp2_index points to the house where the {color:green} condition is fulfilled 
                                if houses[comp2_index + 1].data[comp_key] is None:
                                    assertions.append({comp_key: comp_val, "position": str(comp2_index + 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True   
                            elif comp_index is not None and comp_index - 1 <= 0:
                                # comp_index points to the house where the [color:ivory] condition is fulfilled 
                                if houses[comp_index - 1].data[key2] is None:
                                    # if the house to the right of the house with [color:ivory] has no
                                    # color assigned, its color will be green
                                    assertions.append({key2: clue[key2], "position": str(comp_index - 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True

                        elif "next" in position:
                            print("placeholder: position with next")
                            # clue 11: {"smoke": "kools", "position": "next [pet:horse]"}

                            # right
                            if comp_index is not None and comp_index + 1 < house_number :
                                # comp_index points to the house where the [color:ivory] condition is fulfilled 
                                if houses[comp_index + 1].data[key2] is None:
                                    # if the house to the right of the house with [color:ivory] has no
                                    # color assigned, its color will be green
                                    assertions.append({key2: clue[key2], "position": str(comp_index + 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True
                            elif comp2_index is not None and comp2_index - 1 >= 0:
                                # comp2_index points to the house where the {color:green} condition is fulfilled 
                                if houses[comp2_index - 1].data[comp_key] is None:
                                    assertions.append({comp_key: comp_val, "position": str(comp2_index - 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True

                            # left
                            elif comp2_index is not None and comp2_index + 1 < house_number:
                                # comp2_index points to the house where the {color:green} condition is fulfilled 
                                if houses[comp2_index + 1].data[comp_key] is None:
                                    assertions.append({comp_key: comp_val, "position": str(comp2_index + 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True   
                            elif comp_index is not None and comp_index - 1 <= 0:
                                # comp_index points to the house where the [color:ivory] condition is fulfilled 
                                if houses[comp_index - 1].data[key2] is None:
                                    # if the house to the right of the house with [color:ivory] has no
                                    # color assigned, its color will be green
                                    assertions.append({key2: clue[key2], "position": str(comp_index - 1)})
                                    assertion_used.append(False)
                                    assertion_used[clue_i] = True  

                        else:
                            print("Clue contains invalid position modifier: " + position + ". Exiting...")
                            exit()
        
        if not progress_made:
            print("\n\n\t\tNo progress made in round #" + str(round) + ". Breaking loop.")
            print("\t\tAssertions used: " + str(assertion_used.count(True)) + "/" + str(len(assertion_used))) 
            break
                    
                    
    print("House ##,\tcolor,\tresident,\tpet,\tdrink,\tsmoke")
    for house in houses:
        house.describe()
    



if __name__ == '__main__':
    main()
