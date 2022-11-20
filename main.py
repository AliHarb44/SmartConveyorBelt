import sys
import numpy as np
import math
import random
import time

import gym
import gym_game


def simulate():
    global epsilon, epsilon_decay
    for episode in range(MAX_EPISODES):

        # Init environment
        # Encode the state as an integer and change the states to start from negatives
        state = env.reset()
        total_reward = 0

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):
            # Draw games
            env.render()
            if(episode > 2000):
                time.sleep(0.1)

            stateSave = encode(state)

            # In the beginning, do random action to learn
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[encode(state)])

            # Do action and get result
            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            # Get correspond q value from state, action pair
            q_value = q_table[stateSave][action]
            best_q = np.max(q_table[encode(next_state)])

            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[stateSave][action] = (
                1 - learning_rate) * q_value + learning_rate * (reward + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw games
            env.render()
            if(episode > 2000):
                time.sleep(0.1)

            # When episode is done, print reward
            if done or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f and epsilon = %g." % (
                    episode, t, total_reward, epsilon))
                break

        # exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay


def encode(p):
    y = p[1]
    x = p[0]
    i = x // 2
    if(y % 2 == 0):
        i += (y//2) * 6 + (y//2) * 5
    else:
        i += (y//2) * 6 + (y//2 + 1) * 5
    return i


def decode(i):
    y = 0
    f = True
    while(i >= 5):
        if(f == True):
            i -= 5
            f = False
            y += 1
        else:
            i -= 6
            f = True
            y += 1
    x = i*2
    if(f == True):
        x += 1
    if(x == -1):
        x = 10
        y -= 1
    return([x, y])


if __name__ == "__main__":
    env = gym.make("Pygame-v0")
    MAX_EPISODES = 9999
    MAX_TRY = 1000
    epsilon = 1
    epsilon_decay = 0.998
    learning_rate = 0.1
    gamma = 0.6
    q_table = np.zeros((38, 6))
    simulate()