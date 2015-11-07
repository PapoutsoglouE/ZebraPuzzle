#!/usr/bin/env python
from Household import Household


house_number = 5
houses = list()
for index, house in enumerate(range(house_number)):
	houses.append(Household(index))

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

for house in houses:
	house.describe()

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
	if len(clue) == 2:
		for house in houses:
			key1 = list(clue.keys())[0]  # eg. "person"
			key2 = list(clue.keys())[1]
			if house.data[key1] == clue[key1]:  # if house["person"] = "english"
				house.data[key2] = clue[key2]   # then house["color"] = "red"
			elif house.data[key2] == clue[key2]:
				house.data[key1] = clue[key1]
			else:  # neither clue matches 
			
	# clues that lead to certain conclusions

				
				
#for e in elements:
	#print(e + ":    \t" + str(elements[e]) + "\n")
	


	















