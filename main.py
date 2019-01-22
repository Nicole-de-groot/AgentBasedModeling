# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 09:42:36 2019

@author: Gebruiker
"""

from helpers.modelv4 import Model
import matplotlib.pyplot as plt
import numpy as np

def main():

    modelA = Model()
    modelA.make_buyers()
    modelA.make_sellers()
    modelA.run_simulation()
    
    plt.figure()
	##Plot normal stockflow
    
    #plt.plot(modelA.stock_price_history)
    #plt.show()
    #plt.savefig('results/stock_prices.png')

	##Plot correlation
    list1, list2 = [], []
    for agent in modelA.buyers_list:
        list1.append(agent.profit)
        list2.append(np.std(agent.weights))
    list3, list4 = [], []
    for agent in modelA.sellers_list:
        list3.append(agent.profit)
        list4.append(np.std(agent.weights))
    print(modelA.time)
	
	
    plt.scatter(list1, list2, c="blue")
    plt.scatter(list3, list4, c="green")
    plt.ylabel("Std Weights")
    plt.xlabel("Profit")
    plt.show()

	##Plot matches
    #plt.scatter(modelA.notes_prices_time, modelA.notes_prices_sell, s=3, c="blue")
    #plt.scatter(modelA.notes_prices_time, modelA.notes_prices_buy, s=3, c="green")
    #plt.scatter(modelA.notes_prices_time_match, modelA.notes_prices_match, s=3, c="orange")
    #plt.plot(range(len(modelA.stock_price_history)), modelA.stock_price_history, c="red")
    #plt.show()
    #plt.savefig('results/stock_prices.png')	
	

	
if __name__ == "__main__":
    main()
