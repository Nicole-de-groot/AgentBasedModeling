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
import pandas as pd
import seaborn as sns

#CHECK EXPERIMENTS ON GITHUB:
# Memory vs Profit (agent level)
# Strategy evaluation memory vs Profit (agent level)
# Memory vs Match number (agent level)
# Strategy evaluation memory vs Match number (agent level)
# Feed in real market data --> So how our market deviates
# Seed different markets to check how agents perform in them


#Experiment 1: How does memory influence the market?
#Experiment x: In which kind of market does a
#particular strategy perform better?
#Experiment x: How does memory and strategy influence
#the profit of the agent?
#Experiment x: How well does the agent react on
# a real stock market?
#Experiment x: which strategy works the best for the buyers?
#Experiment x: Which strategy works the best for the sellers?

"""Experiment 1: Memory and profit over time"""
def experiment1():
    memory = [x for x in range(1,6)]
    memory = [1, 5, 10, 30]
    plt.figure()

    for i in memory:
        modelA = main()
        profit_buyer, profit_seller = [], []
        for agent in modelA.buyers_list:
            agent.strategies.memory= i
            profit_buyer.append(agent.profit)
        for agent in modelA.sellers_list:
            agent.strategies.memory = i
            profit_seller.append(agent.profit)
        # index_nr = memory.index(i)
        plt.plot(range(len(profit_buyer)), profit_buyer, label='Buyer m =' + str(i))
        plt.plot(range(len(profit_seller)), profit_seller, label='Seller m =' + str(i))
    plt.title('The profits of agents with different memory')
    plt.xlabel('Time')
    plt.ylabel('Profit')
    plt.legend(loc='best')
    plt.savefig('results/experiment1.png')
    plt.show()


"""Experiment 2: Boxplot memory vs profit"""
def experiment2():
    #Example: http://seaborn.pydata.org/examples/grouped_boxplot.html
    memory, profit, agents = [], [], []
    memories = [x for x in range(1,6)]
    memories = [1,10,20,30]
    random.seed(1)

    for i in memories:
        modelA = Model(0.5)
        modelA.make_buyers(3)
        modelA.make_sellers(3)
        for agent in modelA.buyers_list:
            agent.strategies.memory = i
            memory.append(i)
        for agent in modelA.sellers_list:
            agent.strategies.memory = i
            memory.append(i)

        modelA.run_simulation()

        for agent in modelA.buyers_list:
            profit.append(agent.profit)
            agents.append('Buyer')
        for agent in modelA.sellers_list:
            profit.append(agent.profit)
            agents.append('Seller')

    #Make dataframe and boxplot the results
    sns.set(style="ticks", palette="pastel")
    data = {'Agents': agents, 'Memory': memory, 'Profit': profit}
    df = pd.DataFrame(data, columns=['Agents','Memory','Profit'])
    sns.boxplot(x="Memory", y="Profit",
                hue="Agents", palette=["m", "g"], data=df)
    sns.despine(offset=10, trim=True)
    plt.savefig('results/experiment3.png')
    plt.show()

#def experimentx():
    #Experiment 2 - Strategy evaluation memory vs Profit (agent level)
    #experiment 1 with strategy_evaluation_memory

"""Experiment 3: Artificial and real stock market"""
def run_real_market():
    #Import the data csv file
    #Dataset obtained from: https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/home
    data = []
    df = pd.read_csv('a.us.txt')

    #combine attributes
    #combine high and low by avg
    #combine open and close by avg
    #combine avgHighLow and avgOpenClose
    df['Price'] = (df['High'] + df['Low'] + df['Open'] + df['Close'])/4

    #Drop obsolete columns for faster processing
    drop_columns = ['High', 'Low', 'Open', 'Close', 'Volume','OpenInt']
    df = df.drop(labels=drop_columns, axis=1)

    #Date to datetime and append df to data
    df['Date'] = pd.to_datetime(df['Date'])
    data.append(df)

    # #Plot with pandas - fast
    # print(data)
    # df = df.sort_values('Date') #Just to be sure
    #
    # plt.figure()
    # plt.plot(df['Date'], df['Price'], color='blue', label='Real stock market')
    # plt.title('Stock market')
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.legend(loc='best')
    # plt.show()
    # plt.savefig('results/real_stockmarket.png')

    #Plot with lists - long runtime
    dates = df['Date'].tolist()
    prices = df['Price'].tolist()
    return dates, prices

def experiment3():
    plt.figure()

    dates, prices = run_real_market()
    plt.plot(dates, prices, color='blue', label='Real stock market')
    plt.title('Stock market2')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.savefig('results/experiment5.png')
    plt.show()


"""START PROGRAM"""
def main():
    random.seed(1)
    modelA = Model(0.5)
    modelA.make_buyers(3)
    modelA.make_sellers(3)
    modelA.run_simulation()
    return modelA

if __name__ == "__main__":
    # run experiments
    # experiment1()
    # experiment2()
    # experiment3()
    # experiment4()
    # experiment5()
