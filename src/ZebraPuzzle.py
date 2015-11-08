#!/usr/bin/env python
from Household import Household


house_number = 5
houses = list()
for index, house in enumerate(range(house_number)):
	houses.append(Household(str(index)))

assertions = list()
# each list element is a dictionary with 1 or 2 keys
assertions.append({"person": "english", "color": "red"})                     # 01
assertions.append({"person": "spanish", "pet": "dog"})                       # 02
assertions.append({"drink": "coffee", "color": "green"})                     # 03
assertions.append({"person": "ukrainian", "drink": "tea"})                   # 04
assertions.append({"color": "green", "position": "right [color:ivory]"})     # 05
assertions.append({"color": "ivory"})
assertions.append({"smoke": "old gold", "pet": "snails"})                    # 06
assertions.append({"smoke": "kools", "color": "yellow"})                     # 07
assertions.append({"drink": "milk", "position": "2"})                        # 08
assertions.append({"person": "norwegian", "position": "0"})                  # 09
assertions.append({"smoke": "chesterfields", "position": "next [pet:fox]"})  # 10
assertions.append({"pet": "fox"})
assertions.append({"smoke": "kools", "position": "next [pet:horse]"})        # 11
assertions.append({"pet": "horse"})
assertions.append({"smoke": "lucky strike", "drink": "orange juice"})        # 12 
assertions.append({"person": "japanese", "smoke": "parliaments"})            # 13
assertions.append({"person": "norwegian", "position": "next [color:blue]"})  # 14
assertions.append({"drink": "water"})
assertions.append({"pet": "zebra"})



assertions_c = list(assertions)
compound_assertions = list()

elements = dict()
for clue in assertions:
	
	for key, value in clue.items():
		if key not in elements:
			elements[key] = [value]
		else:
			if value not in elements[key]:
				elements[key].append(value)
	
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
			elif "left" in position:
				print("placeholder: position with left")
			elif "next" in position:
				print("placeholder: position with next")
			elif position.isdigit():
				print("placeholder: position with digit")
			else:
				print("Clue contains invalid position: " + position + ". Exiting...")
				exit()
				
				
#for e in elements:
	#print(e + ":    \t" + str(elements[e]) + "\n")
	


	



for house in houses:
	house.describe()











