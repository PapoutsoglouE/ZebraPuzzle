#!/usr/bin/env python
#from Household import Household
from ProblemData import ProblemData
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
    clues.append({"color": "blue"})
    clues.append({"drink": "water"})
    clues.append({"pet": "zebra"})
    return clues


def check_houses(riddle, clue):
    """ Check how many houses clue1 <-> clue2 could describe.
    Return number of houses, as well as the index of the last house matched. """
    
    possible_placements = 0
    possible_house = None
    possible_fits = 0
    fit_index = None
    # print("Checking houses for clue: " + str(clue))

    for index, house in enumerate(riddle.houses):
        key1, key2 = list(clue.keys())  # eg. "person", "color"
        if house.data[key1] == clue[key1] and house.data[key2] is None:
            # if house["person"] = "english" then house["color"] = "red"
            house.data[key2] = clue[key2] 
            possible_house = index
            possible_placements += 1 
        elif house.data[key2] == clue[key2] and house.data[key1] is None:
            # if house["color"] = "red" then house["person"] = "english"
            house.data[key1] = clue[key1]
            possible_house = index
            possible_placements += 1
        elif house.data[key1] is None and house.data[key2] is None:
            fit_index = index
            possible_fits += 1
        else:  # no way this house is a possible match
            # remove this house from the list of possible houses for this element
            if key1 != "position":
                if index in riddle.elements[key1][clue[key1]]:
                    riddle.elements[key1][clue[key1]].remove(index)
                    #print("removed index " + str(index) + " from " + key1 + ":" + str(clue[key1]))
            if key2 != "position":
                if index in riddle.elements[key2][clue[key2]]:
                    riddle.elements[key2][clue[key2]].remove(index)
                    #print("removed index " + str(index) + " from " + key2 + ":" + str(clue[key2]))
                

    return possible_placements, possible_house, possible_fits, fit_index, riddle


def side_match(rdl, clue_i, idx, kv_pairs):
    key1, val1, key2, val2 = kv_pairs
    progress = False
    if idx[0] is not None and (idx[0] + 1 < rdl.house_number):
        # comp_index points to the house where the [color:ivory] condition is fulfilled 
        if rdl.houses[idx[0] + 1].data[key2] is None:
            # if the house to the right of the house with [color:ivory] has no
            # color assigned, its color will be green
            rdl.assertions.append({key2: val2, "position": str(idx[0] + 1)})
            rdl.assertions_used.append(False)
            rdl.assertions_used[clue_i] = True
            progress = True
    elif idx[1] is not None and idx[1] - 1 >= 0:
        # comp2_index points to the house where the {color:green} condition is fulfilled 
        if rdl.houses[idx[1] - 1].data[key1] is None:
            rdl.assertions.append({key1: val1, "position": str(idx[1] - 1)})
            rdl.assertions_used.append(False)
            rdl.assertions_used[clue_i] = True
            progress = True
    return (rdl, progress)


def deduce(riddle):
    pos_p = re.compile(r"(.*) \[(.*):(.*)\]")  # position pattern
    progress_made = False
    for clue_i, clue in enumerate(riddle.assertions):    
        if not riddle.assertions_used[clue_i]:
            key1, key2 = list(clue.keys())  # eg. "person", "color"
            if "position" not in clue.keys():
                possible_placements, possible_house, fits, fit_index, riddle = check_houses(riddle, clue)
                if possible_placements == 1:  # guaranteed fit, one way or another
                    progress_made = True
                    riddle.assertions_used[clue_i] = True
                    if riddle.houses[possible_house].data[key1] == clue[key1]:
                         # if house["person"] = "english" then house["color"] = "red"
                        riddle.houses[possible_house].data[key2] = clue[key2]
                    else:  # houses[possible_house].data[key2] == clue[key2]
                        # if house["color"] = "red" then house["person"] = "english"
                        riddle.houses[possible_house].data[key1] = clue[key1]
                elif possible_placements == 0 and fits == 1:
                    progress_made = True
                    riddle.houses[fit_index].data[key1] = clue[key1]
                    riddle.houses[fit_index].data[key2] = clue[key2]
                elif fits == 0:
                    print("Cannot possibly fit clue: " + str(clue) + ". Exiting.") 
                    exit()
                    # TODO: handle this possibility better for potential future loop-over 
            else:  # position in clue
                position = clue["position"] # key1 is "position"
                if key2 == "position": key2 = key1 # get other key
                pos_data = re.match(pos_p, position)  # group(1) = "color", group(2) = "ivory 
                if pos_data is None:  # no pattern match
                    if position.isdigit() and int(position) < riddle.house_number:
                        possible_placements, possible_house, fits, fit_index, riddle = check_houses(riddle, clue)
                        if possible_placements == 1:  # guaranteed fit, one way or another
                            progress_made = True
                            riddle.assertions_used[clue_i] = True
                            if riddle.houses[possible_house].data["position"] == clue["position"]:
                                 # if house["person"] = "english" then house["color"] = "red"
                                riddle.houses[possible_house].data[key2] = clue[key2]
                            else:  # houses[possible_house].data[key2] == clue[key2]
                                # if house["color"] = "red" then house["person"] = "english"
                                riddle.houses[possible_house].data["position"] = clue["position"]
                        elif possible_placements == 0 and fits == 1:
                            progress_made = True
                            riddle.houses[fit_index].data[key1] = clue[key1]
                            riddle.houses[fit_index].data[key2] = clue[key2]
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
                    pos_progress_made = False
                    pos_modifier, comp_key, comp_val = pos_data.groups()  # comparison key: color, comparison value: ivory
                    # clue[key2] = green, key2 = color
                    # comp_key = color, comp_val = ivory
                    comp_index, comp2_index = None, None  
                    # index of house with color = ivory, color = green
                    # example: {"color": "green", "position": "right [color:ivory]" 
                    
                    if not pos_modifier in ["right", "left", "next"]:
                        print("Clue contains invalid position modifier: " + position + ". Exiting...")
                        exit()

                    for i, h in enumerate(riddle.houses):
                        if h.data[comp_key] == comp_val:  # if color = ivory
                            comp_index = i
                        if h.data[key2] == clue[key2]:  # if color = green
                            comp2_index = i

                    if pos_modifier in ["right", "next"]:
                        if pos_modifier == "right":
                            if 0 in riddle.elements[key2][clue[key2]]:
                                print("Stating that the " + clue[key2] + " " + key2 + " can't be at 0.")
                                riddle.elements[key2][clue[key2]].remove(0)
                            for i, h in enumerate(riddle.houses): 
                                # if the house on the right is not green, the house on its left is not ivory.
                                if i == 0: continue
                                if h.data[key2] != clue[key2] and h.data[key2] is not None:
                                    if (i - 1) in riddle.elements[comp_key][comp_val]:
                                        print("Stating that the " + comp_key + " " + comp_val + " can't be at " + str(i-1))
                                        riddle.elements[comp_key][comp_val].remove(i-1)

                                # if the house on the left is not ivory, the house on the right is not green
                                if i == riddle.house_number - 1: continue
                                if h.data[comp_key] != comp_val and h.data[comp_key] is not None:
                                    if (i + 1) in riddle.elements[key2][clue[key2]]:
                                        print("Stating that the " + key2 + " " + clue[key2] + " can't be at " + str(i+1))
                                        riddle.elements[key2][clue[key2]].remove(i-1)

                        riddle, pos_progress_made = side_match(riddle, clue_i, [comp_index, comp2_index], 
                                                               [comp_key, comp_val, key2, clue[key2]])
                    if pos_modifier == "left" or (pos_modifier == "next" and not pos_progress_made):
                        if pos_modifier == "left":
                            if (riddle.house_number - 1) in riddle.elements[key2][clue[key2]]:
                                print("Stating that the " + clue[key2] + " " + key2 + " can't be at 5.")
                                riddle.elements[key2][clue[key2]].remove(riddle.house_number - 1)
                        riddle, pos_progress_made = side_match(riddle, clue_i, [comp2_index, comp_index], 
                                                               [key2, clue[key2], comp_key, comp_val])


                    cl_prog_made = riddle.clean_elements()
                    progress_made = pos_progress_made or progress_made or cl_prog_made
    
    return riddle, progress_made


def eliminate():
    pass


def main():
    """ Solve riddle. """
    house_number = 5
    riddle = ProblemData(house_number, build_assertions())

    for rounds in range(15):
        progress_made = False  # have any changes (progress) been made this round?
        riddle, progress_made = deduce(riddle)
        if not progress_made:
            print("\t\tNo progress made in round #" + str(rounds + 1) + ". Breaking loop.")
            print("\t\tAssertions used: " + str(riddle.assertions_used.count(True)) + "/" 
                  + str(len(riddle.assertions_used))) 
            break


    riddle.house_state()
    riddle.element_state()




if __name__ == '__main__':
    main()
