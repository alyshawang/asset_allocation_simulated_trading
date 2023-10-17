import gym
from gym import spaces
import numpy as np
import pandas as pd
import yfinance as yf

import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleTradingEnv(gym.Env):
    def __init__(self, stock_tickers, start_date, end_date):
        super(SimpleTradingEnv, self).__init__()

        self.stock_tickers = stock_tickers
        self.num_stocks = len(stock_tickers)

        self.observation_space = spaces.Box(low = 0, high = 1, shape = (self.num_stocks, ))
        self.action_space = spaces.Discrete(self.num_stocks + 1)

        self.current_step = 0
        self.start_date = start_date
        self.end_date = end_date
        self.prices = self._download_prices()
        self.max_steps = len(self.prices)

    def _download_prices(self):
        stock_data = yf.download(self.stock_tickers, start = self.start_date,
            end = self.end_date)
        return stock_data['Close']

    def reset(self):
        self.current_step = 0
        observation = self._get_observation()
        return observation

    def step(self, action):
        self.current_step += 1
        done = self.current_step >= self.max_steps

        observation = self._get_observation()

        # Implement reward function
        reward = 0.0

        # specify information fields to use in steps
        info = {}

        return observation, reward, done, info

    def _get_observation(self):
        start_index = self.current_step
        end_index = min(self.current_step + 10, self.max_steps)

        if end_index <= start_index:
            observation = np.zeros((self.num_stocks,))
        else:
            stock_prices = self.prices.iloc[start_index:end_index].values
            observation = stock_prices.flatten()

        return observation

    def render(self, mode='human'):
        # Implement rendering if needed
        pass

    def close(self):
        # Implement any cleanup operations
        pass

if __name__ == "__main__":
    stock_tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    crypto_tickers = ["BNB-USD", 'BTC-USD']
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    env = SimpleTradingEnv(stock_tickers, start_date, end_date)
    observation = env.reset()

    for step in range(env.max_steps):
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)

        print(f"Step: {step}")
        print(f"Observation: {observation}")
        print(f"Reward: {reward}")
        print(f"Done: {done}")

        if done:
            break

    env.close()
