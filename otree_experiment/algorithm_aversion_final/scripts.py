#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 16:46:39 2022

@author: vinicius.ferraz
"""

import random as rd
import string


#%%



#%% Algorithm for Flatenning Multi-level Lists (used in treatment split)

def flat(pool):
    res = []
    for v in pool:
        if isinstance(v, list):
          res += flat(v)
        else:
          if isinstance(v, int):
            res.append(v)
    return res 

#%% Algorithm for Balanced Randomization of Treatments

def treatments_gen(number_players, treatment_possibilities):
    treatments_list, final_list = [], []
    while len(final_list) < (number_players):
        rd_list = rd.sample(range(1,treatment_possibilities+1), treatment_possibilities)
        treatments_list.append(rd_list)
        final_list = flat(treatments_list)
    return final_list
#%%

# Function for lower case + numbers
def name_gen_LC(lenght):
    name = "".join(rd.choices(string.ascii_lowercase + string.digits, k=lenght))
    return name