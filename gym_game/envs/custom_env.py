import gym
from gym import spaces
import numpy as np
from gym_game.envs.pygame_2d import PyGame2D2


class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = PyGame2D2()
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(
            np.array([0, 0]), np.array([10, 6]), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = PyGame2D2()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()