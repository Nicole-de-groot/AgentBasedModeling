# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 09:42:36 2019

@author: Gebruiker
"""

from helpers.modelv4 import Model
from helpers.make_csv import make_csv
import matplotlib.pyplot as plt
import numpy as np
import random


def main():

    random.seed(4)
    modelA = Model(0.5)
    modelA.make_buyers(3)
    modelA.make_sellers(3)
    modelA.run_simulation()

    print(modelA.buyers_list[-1].strategy_index)
    plt.figure()
	##Plot normal stockflow

    #plt.plot(modelA.stock_price_history)
    #plt.show()
    #plt.savefig('results/stock_prices.png')

	##Plot correlation
    #list1, list2 = [], []
    #for agent in modelA.buyers_list:
    #    list1.append(agent.profit)
    #    list2.append(agent.memory)
    #list3, list4 = [], []
    #for agent in modelA.sellers_list:
    #    list3.append(agent.profit)
    #    list4.append(agent.memory)
    #print(modelA.time)
	#
	#
    #plt.scatter(list2, list1, c="blue")
    #plt.scatter(list4, list3, c="green")
    #plt.ylabel("Profit")
    #plt.xlabel("Memory")
    #plt.show()
    #plt.savefig('results/crossreverence.png')

	#Plot matches
	
   
	
    plt.scatter(modelA.notes_prices_time_sellers, modelA.notes_prices_sell, s=3, c="blue")
    plt.scatter(modelA.notes_prices_time_buyers, modelA.notes_prices_buy, s=3, c="green")
    plt.scatter(modelA.notes_prices_time_match, modelA.notes_prices_match, s=3, c="orange")
    plt.plot(range(len(modelA.stock_price_history)), modelA.stock_price_history, c="red")
    plt.axis(ymin = 0)
    plt.show()
    plt.savefig('results/stock_prices.png')
	
    make_csv(modelA)
	

	
if __name__ == "__main__":
    main()
