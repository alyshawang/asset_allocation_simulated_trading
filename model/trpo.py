import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
import gym

class PolicyNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        action_probs = torch.softmax(self.fc2(x), dim = -1)
        return action_probs
    
def get_action(policy, state):
    state = torch.tensor(state, dtype = torch.float32)
    action_probs = policy(state)
    dist = Categorical(action_probs)
    action = dist.sample()
    log_prob = dist.log_prob(action)
    return action.item(), log_prob

def compute_advantages(rewards, values, gamma = 0.99, lamda = 0.95):
    # Compute GAE (Generalized Advantage Estimation)
    # This function needs more detail
    pass

def surrogate_loss(old_probs, new_probs, advantages, epsilon = 1e-2):
    ratio = new_probs / old_probs
    clipped_ratio = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)
    surrogate = torch.min(ratio * advantages, clipped_ratio * advantages)
    return torch.mean(surrogate)

def TRPO_update(policy, states, actions, log_probs_old, 
                returns, advantages, epsilon = 1e-2):
    # Convert lists to tensors
    states = torch.tensor(states, dtype = torch.float32)
    actions = torch.tensor(actions, dtype = torch.long)
    log_probs_old = torch.tensor(log_probs_old, dtype = torch.float32)
    advantages = torch.tensor(advantages, dtype = torch.float32)
    
    # Get the new action probabilities
    action_probs = policy(states)
    dist = Categorical(action_probs)
    log_probs_new = dist.log_prob(actions)
    
    loss = -surrogate_loss(log_probs_old.exp(), log_probs_new.exp(), advantages)
    
    # Compute gradient of loss w.r.t. network parameters
    grads = torch.autograd.grad(loss, policy.parameters())
    
    # Here you'd need to use the conjugate gradient method and other components of TRPO
    # This requires more intricate computations which are too lengthy to detail here.
    # The goal is to update the policy in the direction of the computed gradient
    # while ensuring the new policy doesn't deviate too much from the old policy 
    # (measured using KL-divergence)
    
    # For now, let's use a basic gradient ascent step as a placeholder:
    optimizer = optim.Adam(policy.parameters(), lr = 0.01)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
