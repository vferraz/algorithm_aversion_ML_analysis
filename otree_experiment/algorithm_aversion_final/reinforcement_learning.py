#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:10:35 2022

@author: vinicius.ferraz
"""

# Reinforcament Learning Model for Algorithm Aversion

import math
import random



def product_selection(prob_1, prob_2, prob_3):
    strat_i = random.choices(
        population = [1, 2, 3],
        weights = [prob_1, prob_2, prob_3],
        k = 1)
    return strat_i[0]

def prob_gen(lam, A_1, A_2, A_3):
    prob_prod_1 = math.exp(lam * A_1) / (math.exp(lam * A_1) + math.exp(lam * A_2) + math.exp(lam * A_3))
    prob_prod_2 = math.exp(lam * A_2) / (math.exp(lam * A_1) + math.exp(lam * A_2) + math.exp(lam * A_3))
    prob_prod_3 = math.exp(lam * A_3) / (math.exp(lam * A_1) + math.exp(lam * A_2) + math.exp(lam * A_3))
    return prob_prod_1, prob_prod_2, prob_prod_3

def rl_attraction(phi, A, payoff):
    A_new = phi * A + payoff
    return A_new

def reinforcement_learning_update(phi, payoff_1, payoff_2, payoff_3, attrac_1, attrac_2, attrac_3):
    attrac_1 = rl_attraction(phi, attrac_1, payoff_1) 
    attrac_2 = rl_attraction(phi, attrac_2, payoff_2)
    attrac_3 = rl_attraction(phi, attrac_3, payoff_3)  
    return attrac_1, attrac_2, attrac_3


# phi = RECENCY - indicates the speed at which past payoffs are forgotten. 
# If phi=0, only the payoff from the last round matters; if phi=1, payoffs from all previous rounds matter equally.