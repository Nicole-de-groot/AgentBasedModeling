# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 09:44:23 2019

@author: Gebruiker
"""

# agent - old agent file -- smartagent - new agent file
from classes.secretAgent import Agent
import random

class Model():

    def __init__(self):

        self.time = 0
        self.end_time = 1000
        self.matching_rounds = 10

        self.buyers_list = []
        self.sellers_list = []

        self.number_of_buyers = 100
        self.number_of_sellers = 100
        self.ratio_of_smart_agents = 0.5

        self.stock_price = 10
        self.stock_price_history = [10]

        self.temp_stock_price = 0

        # Warming-up parameters
        self.warming_up_time = 100
        self.number_of_wu_agents = 10
        self.warm_up_buyers_list = []
        self.warm_up_sellers_list = []

        #Parameters for plotting notes Jasper
        self.notes_prices_time = [] #NOTES
        self.notes_prices_time_sellers = []
        self.notes_prices_time_buyers = []
        self.notes_prices_sell = []
        self.notes_prices_buy = []
        self.notes_prices_match = []
        self.notes_prices_time_match = []

    """
    Make the Agents buyers and sellers
    Buyers are False, sellers are True
    """
    def make_buyers(self):
        for i in range(self.number_of_buyers):
            self.buyers_list.append(Agent(False))

    def make_sellers(self):
        for i in range(self.number_of_sellers):
            self.sellers_list.append(Agent(True))


    """Start running the simulation"""
    def run_simulation(self):
        #Append the warming up agents
        for i in range(self.number_of_wu_agents):
            self.warm_up_buyers_list.append(Agent(False))
            self.warm_up_sellers_list.append(Agent(True))

		#Warming up period
        while(self.time < self.warming_up_time):
            for i in range(self.number_of_wu_agents):
                self.warm_up_buyers_list[i].random_choose(self.stock_price_history)
                self.warm_up_sellers_list[i].random_choose(self.stock_price_history)

            winning_agents = []
            temp_buyers =  self.warm_up_buyers_list.copy()
            temp_sellers = self.warm_up_sellers_list.copy()

            #Match the buyers and sellers
            winning_agents, temp_buyers, temp_sellers = self.match(winning_agents, temp_buyers, temp_sellers)

            #Update the stock price based on the match
            self.stock_price = self.temp_stock_price / (len(winning_agents) / 2)
            self.stock_price_history.append(self.stock_price)

            self.temp_stock_price = 0
            self.time += 1

        #Start the real simulation
        while(self.time < self.end_time + self.warming_up_time):
            for buyer in self.buyers_list[round((self.ratio_of_smart_agents*self.number_of_buyers)):]:
                buyer.choose(self.stock_price_history)
            for buyer in self.buyers_list[:round((self.ratio_of_smart_agents*self.number_of_buyers))]:
                buyer.random_choose(self.stock_price_history)

            for seller in self.sellers_list[round(self.ratio_of_smart_agents*self.number_of_sellers):]:
                seller.choose(self.stock_price_history)
            for seller in self.sellers_list[:round(self.ratio_of_smart_agents*self.number_of_sellers)]:
                seller.random_choose(self.stock_price_history)

            #print([[agent.buy_prices[-1], agent.memory] for agent in temp_buyers])

            winning_agents = []
            temp_buyers = self.buyers_list.copy()
            temp_sellers = self.sellers_list.copy()

            #Match the buyers and sellers
            winning_agents, temp_buyers, temp_sellers = self.match(winning_agents, temp_buyers, temp_sellers)

            #Update the stock price based on the match
            self.stock_price = self.temp_stock_price / (len(winning_agents) / 2)
            self.stock_price_history.append(self.stock_price)

            self.temp_stock_price = 0
            self.time += 1

            #Update function could be implemented in calcProfit
            # for buyer in self.buyers_list:
            #     if buyer in winning_agents:
            #         buyer.update(True, self.stock_price)
            #     else:
            #         buyer.update(False, self.stock_price)
            #
            # for seller in self.sellers_list:
            #     if seller in winning_agents:
            #         seller.update(True, self.stock_price)
            #     else:
            #         seller.update(False, self.stock_price)

            #Calculate the profit of the agents
            for buyer in self.buyers_list:
                buyer.calcProfit(self.stock_price_history[-1])

            for seller in self.sellers_list:
                seller.calcProfit(self.stock_price_history[-1])


    """Match the Agents buyers and sellers"""
    #Define the shortest and longest list of buyers and sellers
    #Since the amount of buyers and sellers could be different
    def define_lists(self, temp_buyers, temp_sellers):
        shortest_list = temp_sellers
        longest_list = temp_buyers
        if (len(temp_buyers) < len(temp_sellers)):
            shortest_list = temp_buyers
            longest_list = temp_sellers
        return shortest_list, longest_list

    #Match the Agents buyers and sellers
    def match(self, winning_agents, temp_buyers, temp_sellers):
        #Define of the buyers and sellers list which one is the shortest and longest
        shortest_list, longest_list = self.define_lists(temp_buyers, temp_sellers)

        #Notes Jasper
        # for i in range(len(temp_sellers)):
        #     self.notes_prices_time_sellers.append(self.time)
        #     self.notes_prices_sell.append(temp_sellers[i].sell_prices[-1])
        #
        # for j in range(len(temp_buyers)):
        #     self.notes_prices_time_buyers.append(self.time)
        #     self.notes_prices_buy.append(temp_buyers[j].buy_prices[-1])

        #Starting parameters, winning is a match
        winning_indices = []
        random.shuffle(temp_sellers)
        random.shuffle(temp_buyers)

        #When the sell price is smaller than the buy price, then there is a match
        #Add the average of those prices to the stock price
        for i in range(len(shortest_list)):
            if (temp_sellers[i].sell_prices[-1] <= temp_buyers[i].buy_prices[-1]):
                winning_indices.append(i)

                temp_sellers[i].matched((temp_sellers[i].sell_prices[-1] + temp_buyers[i].buy_prices[-1]) / 2)
                temp_buyers[i].matched((temp_sellers[i].sell_prices[-1] + temp_buyers[i].buy_prices[-1]) / 2)
                self.temp_stock_price += (temp_sellers[i].sell_prices[-1] + temp_buyers[i].buy_prices[-1]) / 2

                #Notes Jasper
                # self.notes_prices_match.append(temp_sellers[i].sell_prices[-1])
                # self.notes_prices_match.append(temp_buyers[i].buy_prices[-1])
                # self.notes_prices_time_match.append(self.time)

        #Append the matching agents to the winning agents
        #And delete those from the temporary lists
        for i in sorted(winning_indices, reverse=True):
            winning_agents.append(temp_buyers[i])
            winning_agents.append(temp_sellers[i])
            del temp_buyers[i]
            del temp_sellers[i]

        #Continue on finding matches
        winning_indices = []

        for i in range(len(temp_sellers)):
            for j in range(len(temp_buyers)):
                if temp_sellers[i].sell_prices[-1] <= temp_buyers[j].buy_prices[-1]:
                    winning_indices.append(i)

                    temp_sellers[i].matched((temp_sellers[i].sell_prices[-1] + temp_buyers[j].buy_prices[-1]) / 2)
                    temp_buyers[j].matched((temp_sellers[i].sell_prices[-1] + temp_buyers[j].buy_prices[-1]) / 2)
                    self.temp_stock_price += (temp_sellers[i].sell_prices[-1] + temp_buyers[j].buy_prices[-1]) / 2

                    #Notes Jasper
                    # self.notes_prices_match.append(temp_sellers[i].sell_prices[-1])
                    # self.notes_prices_match.append(temp_buyers[j].buy_prices[-1])
                    # self.notes_prices_time_match.append(self.time)


                    #Append the matching buyers to the winning agents
                    #And delete those from the temporary list
                    winning_agents.append(temp_buyers[j])
                    del temp_buyers[j]
                    break

        #Append the matching sellers to the winning agents
        #And delete those from the temporary list
        for i in sorted(winning_indices, reverse=True):
            winning_agents.append(temp_sellers[i])
            del temp_sellers[i]

        return winning_agents, temp_buyers, temp_sellers

#OLD CODE OF MATCH
#Match the Agents buyers and sellers
def match2(self, winning_agents, temp_buyers, temp_sellers):
    shortest_list, longest_list = self.define_lists(temp_buyers, temp_sellers)

    for i in range(len(temp_sellers)):
        self.notes_prices_time.append(self.time)
        self.notes_prices_sell.append(temp_sellers[i].sell_prices[-1])
        self.notes_prices_buy.append(temp_buyers[i].buy_prices[-1])


    #print("shortest",shortest_list)
    #print("longest",longest_list)
    #print("sell",temp_sellers)
    #print("buy",temp_buyers)

    winning_indices = []
    random.shuffle(temp_sellers)
    random.shuffle(temp_buyers)
    for i in range(len(shortest_list)):
        if (temp_sellers[i].sell_prices[-1] <= temp_buyers[i].buy_prices[-1]):
            winning_indices.append(i)

            temp_sellers[i].matched((temp_sellers[i].sell_prices[-1] + temp_buyers[i].buy_prices[-1]) / 2)
            temp_buyers[i].matched((temp_sellers[i].sell_prices[-1] + temp_buyers[i].buy_prices[-1]) / 2)
            self.temp_stock_price += (temp_sellers[i].sell_prices[-1] + temp_buyers[i].buy_prices[-1]) / 2

            self.notes_prices_match.append(temp_sellers[i].sell_prices[-1])
            self.notes_prices_match.append(temp_buyers[i].buy_prices[-1])
            self.notes_prices_time_match.append(self.time)
            self.notes_prices_time_match.append(self.time) #WHY?

    for i in sorted(winning_indices, reverse=True):
        winning_agents.append(temp_buyers[i])
        winning_agents.append(temp_sellers[i])
        del temp_buyers[i]
        del temp_sellers[i]

    winning_indices = []

    for i in range(len(temp_sellers)):
        for j in range(len(temp_buyers)):
            if temp_sellers[i].sell_prices[-1] <= temp_buyers[j].buy_prices[-1]:
                winning_indices.append(i)
                self.temp_stock_price += (temp_sellers[i].sell_prices[-1] + temp_buyers[j].buy_prices[-1]) / 2
                self.notes_prices_match.append(temp_sellers[i].sell_prices[-1])
                self.notes_prices_match.append(temp_buyers[j].buy_prices[-1])
                self.notes_prices_time_match.append(self.time)
                self.notes_prices_time_match.append(self.time) #WHY?
                winning_agents.append(temp_buyers[j])
                del temp_buyers[j]
                break

    for i in sorted(winning_indices, reverse=True):
        winning_agents.append(temp_sellers[i])
        del temp_sellers[i]

    return winning_agents, temp_buyers, temp_sellers
