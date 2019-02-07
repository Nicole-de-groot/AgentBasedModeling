# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 09:44:23 2019

@author: Gebruiker
"""

# agent - old agent file -- smartagent - new agent file
from classes.agentv7 import Agent
import random
import math
import classes.properties as properties

class Model():

    def __init__(self, random_agent):

        """runtime"""
        self.time = 0
        self.end_time = properties.max_runtime

        """list of the agents"""
        self.buyers_list = []
        self.sellers_list = []

        """constants"""
        self.number_of_buyers = properties.number_of_buyers
        self.number_of_sellers = properties.number_of_sellers
        self.ratio_of_random_agents = random_agent
        self.id_counter = 0
		
        """stock prices"""
        self.stock_price_history = [properties.initial_stockprice]

        """to see what is the best price every turn"""
        self.best_sell_price = [self.stock_price_history[0]]
        self.best_buy_price = [self.stock_price_history[0]]

        """temporary stock price to calculate next stock price in the market"""
        self.temp_stock_price = 0

        """Warming-up parameters"""
        self.warming_up_time = properties.warming_up_time
        self.number_of_wu_agents = properties.number_of_wu_agents
        self.warm_up_buyers_list = []
        self.warm_up_sellers_list = []

        """Parameters for plotting"""
        self.plots_prices_time_sellers = []
        self.plots_prices_time_buyers = []
        self.plots_prices_sell = []
        self.plots_prices_buy = []
        self.plots_prices_match = []
        self.plots_prices_time_match = []	

    """
    Make the Agents buyers and sellers
    Buyers are False, sellers are True
    """
    def make_buyers(self,strategy_number,allrandom=False):

        randoms = int(round((self.ratio_of_random_agents*self.number_of_buyers)))
        
        for i in range(randoms):
            self.buyers_list.append(Agent(False, self.id_counter, strategy_number,True))
            self.id_counter += 1
        
        for i in range(self.number_of_sellers-randoms):
            self.buyers_list.append(Agent(False, self.id_counter, strategy_number,False))
            self.id_counter += 1

    def make_sellers(self,strategy_number,allrandom=False):
        
        randoms = int(round((self.ratio_of_random_agents*self.number_of_sellers)))
        
        for i in range(randoms):
            self.sellers_list.append(Agent(True, self.id_counter, strategy_number,True))
            self.id_counter += 1
        
        for i in range(self.number_of_sellers-randoms):
            self.sellers_list.append(Agent(True, self.id_counter, strategy_number,False))
            self.id_counter += 1

    def update_market(self, buyers_list, sellers_list):

        """copy lists to determine which agents matched up"""
        winning_agents = []
        temp_buyers =  buyers_list.copy()
        temp_sellers = sellers_list.copy()

        """match the buyers and sellers"""
        winning_agents, temp_buyers, temp_sellers = self.match(winning_agents, temp_buyers, temp_sellers)

        """update the stock price based on the match"""
        if len(winning_agents) == 0:
            self.stock_price_history.append(self.stock_price_history[-1]
        else:
            if self.time <= self.warming_up_time / 2.0:
                self.temp_stock_price = (self.temp_stock_price / (len(winning_agents) / 2))
         else:
                self.temp_stock_price = (self.temp_stock_price / (len(winning_agents) / 2))

            self.stock_price_history.append(self.temp_stock_price)

        self.temp_stock_price = 0
        self.time += 1
    
    """match the agents: buyers and sellers"""
    def match(self, winning_agents, temp_buyers, temp_sellers):

        """plots of the prices of sellers and buyers"""
        for i in range(len(temp_sellers)):
            self.plots_prices_time_sellers.append(self.time)
            self.plots_prices_sell.append(temp_sellers[i].sell_prices[-1])

        for j in range(len(temp_buyers)):
            self.plots_prices_time_buyers.append(self.time)
            self.plots_prices_buy.append(temp_buyers[j].buy_prices[-1])

        """starting parameters, winning is a match"""
        winning_indices = []
        random.shuffle(temp_sellers)
        random.shuffle(temp_buyers)
		
        self.best_sell_price.append(temp_sellers[0].sell_prices[-1])
        self.best_buy_price.append(temp_buyers[0].buy_prices[-1])

        """the match up algorithm"""
        for i in range(len(temp_sellers)):
            for j in range(len(temp_buyers)):
                if temp_sellers[i].sell_prices[-1] <= temp_buyers[j].buy_prices[-1]:

                    """find the best prices each turn"""
                    if self.best_sell_price[-1] < temp_sellers[i].sell_prices[-1]:
                        self.best_sell_price[-1] = temp_sellers[i].sell_prices[-1]
                    if self.best_buy_price[-1] > temp_buyers[j].buy_prices[-1]:
                        self.best_buy_price[-1] = temp_buyers[j].buy_prices[-1] 
					
                    winning_indices.append(i)

                    average_price = (temp_sellers[i].sell_prices[-1] + temp_buyers[j].buy_prices[-1]) / 2
                    temp_sellers[i].matched(average_price)
                    temp_buyers[j].matched(average_price)
                    self.temp_stock_price += average_price

                    """plots of the prices of matches"""
                    self.plots_prices_match.append(temp_sellers[i].sell_prices[-1])
                    self.plots_prices_match.append(temp_buyers[j].buy_prices[-1])
                    self.plots_prices_time_match.append(self.time)  #For the matched seller
                    self.plots_prices_time_match.append(self.time) #For the matched buyer

                    """append the matching buyers to the winning agents
                       and delete those from the temporary list"""
                    winning_agents.append(temp_buyers[j])
                    del temp_buyers[j]
                    break

        """append the matching sellers to the winning agents
           and delete those from the temporary list"""
        for i in sorted(winning_indices, reverse=True):
            winning_agents.append(temp_sellers[i])
            del temp_sellers[i]

        return winning_agents, temp_buyers, temp_sellers

    """start warm-up period"""
    def warm_up(self):

        """create warm-up agents"""
        for i in range(self.number_of_wu_agents):
            self.warm_up_buyers_list.append(Agent(False, self.id_counter,1,True))
            self.warm_up_sellers_list.append(Agent(True, self.id_counter,1,True))

        """warming up period"""
        while(self.time < self.warming_up_time):
            for i in range(self.number_of_wu_agents):
                self.warm_up_buyers_list[i].random_choose(self.stock_price_history)
                self.warm_up_sellers_list[i].random_choose(self.stock_price_history)

            self.update_market(self.warm_up_buyers_list, self.warm_up_sellers_list)

    """run the stock market"""
    def run_simulation(self):
        
        for buyer in self.buyers_list:
            buyer.initial_track_strategies(self.stock_price_history)
        for seller in self.sellers_list:
            seller.initial_track_strategies(self.stock_price_history)

        """agents determine new sell/buy price and are matched up accordingly"""
        while(self.time < self.end_time + self.warming_up_time):
            for buyer in self.buyers_list:
                if not buyer.random:
                    buyer.match_prices.append(0)
                    buyer.track_strategies(self.stock_price_history, self.best_buy_price[-1])
                    buyer.buy_prices.append(buyer.choose(self.stock_price_history, buyer.choose_strategy()))
                else:
                    if random.random() > 0.9:
                        buyer.fixed_choose(self.stock_price_history)
                    else:
                        buyer.random_choose(self.stock_price_history)

            for seller in self.sellers_list:
                if not seller.random:
                    seller.match_prices.append(0)
                    seller.track_strategies(self.stock_price_history, self.best_sell_price[-1])
                    seller.sell_prices.append(seller.choose(self.stock_price_history, seller.choose_strategy()))
                else:
                    if random.random() > 0.9:
                        seller.fixed_choose(self.stock_price_history)
                    else:
                        seller.random_choose(self.stock_price_history)

            self.update_market(self.buyers_list, self.sellers_list)
