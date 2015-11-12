#!/usr/bin/env python

class Household():
    def __init__(self, position=None):
        self.data = {"person": None, "pet": None,
                     "drink": None, "smoke": None,
                     "color": None}
        self.data["position"] = str(position) if str(position) is not None else None                 
        # position is a string!
    
    def describe(self):
        pos = self.cn(self.data["position"])
        col = self.cn(self.data["color"])
        prs = self.cn(self.data["person"])
        pet = self.cn(self.data["pet"])
        drk = self.cn(self.data["drink"])
        smk = self.cn(self.data["smoke"])
        #print("House #" + str(pos) + " is " + col + ",")
        #print("\tbelongs to a " + prs + ", ")
        #print("\thas a " + pet + " as a pet,")
        #print("\tdrinks " + drk + " and smokes " + smk + ".\n")
        print("House #" + str(pos) + ":\t" + col + ",\t" + prs + ",\t"
               + pet + ",\t" + drk + ",\t" + smk)
    

    def isEmpty(self):
        if not None in self.data.values():
            return False
        else:
            return True
            
        
    @staticmethod
    def cn(string_to_verify):
        if string_to_verify is None:
            return "[?]"
        else:
            return string_to_verify
            
