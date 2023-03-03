import os
import sys
base_path = os.path.dirname(__file__)
sys.path.append(base_path + "/..")

import argparse
import os
import time

import gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.noise import (NormalActionNoise,
                                            OrnsteinUhlenbeckActionNoise)
from environments import jsbsim_gym
from gym import envs
print(envs.registry.all())

def parse_args():
    parser = argparse.ArgumentParser(description='TBD')
    parser.add_argument('--playSpeed', default=0, metavar='double', help='specifies to run in real world time')
    parser.add_argument('--trainPolicy', default='Level', metavar='string', help='specifies the opposite plane\'s strategy of dogfighting')
    parser.add_argument('--train', default=False, action='store_true', help='specifies the running mode of DBRL')
    parser.add_argument('--test', default=True, action='store_true', help='specifies the running mode of DBRL')
    parser.add_argument('--timesteps', default=1_000_000, metavar='int', help='specifies the training timesteps. Only works when --train is specified')
    args = parser.parse_args()
    return args

args = parse_args()

print(f'\n{args = }')

env = gym.make(
    "JsbsimEnv-v0",
    policy2=args.trainPolicy
)

n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

model = SAC(
    "MlpPolicy",
    env, 
    verbose=1,
    action_noise=action_noise,
)

path = r'./log/'
if not os.path.exists(path):
    os.mkdir(path)

if args.train:
    # try:
    #     model.set_parameters("./log/sac_jsbsim")
    # except:
    #     pass
    model.learn(total_timesteps=int(args.timesteps), log_interval=1)
    model.save("./log/sac_jsbsim")

if args.test:
    model = SAC.load("./log/sac_jsbsim")

    win = 0
    episode = 0

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()
        if dones == True:
            f = open('./log/sac_jsbsim_record.txt', 'a')
            if rewards == 50:
                win += 1
            episode += 1
            f.write("{} / {}\n".format(win, episode))
            print("Done! episode: {}\tacc: {}".format(episode, win / episode))
            time.sleep(2)
            env.reset()
