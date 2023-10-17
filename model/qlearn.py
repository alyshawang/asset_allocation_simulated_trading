import numpy as np
from env import main

class QLearningAgent:
    def __init__(self, n_actions, n_states, learning_rate = 0.1, discount_factor = 0.9, epsilon = 0.1):
        self.n_actions = n_actions
        self.n_states = n_states
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

        # Initialize Q-table with zeros
        self.q_table = np.zeros((n_states, n_actions))

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.n_actions)  # Explore
        else:
            return np.argmax(self.q_table[state, :])  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        predict = self.q_table[state, action]
        target = reward + self.discount_factor * np.max(self.q_table[next_state, :])
        self.q_table[state, action] += self.learning_rate * (target - predict)

if __name__ == "__main__":
    stock_tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    env = main.SimpleTradingEnv(stock_tickers, start_date, end_date)
    observation = env.reset()

    n_actions = env.action_space.n
    n_states = env.observation_space.shape[0]
    
    agent = QLearningAgent(n_actions, n_states)

    for step in range(env.max_steps):
        action = agent.select_action(observation)
        next_observation, reward, done, _ = env.step(action)

        agent.update_q_table(observation, action, reward, next_observation)

        observation = next_observation

        print(f"Step: {step}")
        print(f"Observation: {observation}")
        print(f"Action: {action}")
        print(f"Reward: {reward}")
        print(f"Done: {done}")

        if done:
            break

    env.close()
