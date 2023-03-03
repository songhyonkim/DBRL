import argparse
import os
import time

import gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.noise import (NormalActionNoise,
                                            OrnsteinUhlenbeckActionNoise)


# def parse_args():
#     parser = argparse.ArgumentParser(description='TBD')
#     parser.add_argument('--host', default='10.184.0.0', metavar='str', help='specifies Harfang host id')
#     parser.add_argument('--port', default='50888', metavar='str', help='specifies Harfang port id')
#     parser.add_argument('--planeSlot', default=1, metavar='int', help='specifies the ego plane')
#     parser.add_argument('--enemySlot', default=3, metavar='int', help='specifies the enemy plane')
#     parser.add_argument('--missileSlot', default=1, metavar='int', help='specifies the missile')
#     parser.add_argument('--playSpeed', default=0, metavar='double', help='specifies to run in real world time')
#     parser.add_argument('--train', action='store_true', help='specifies the running mode of DBRL')
#     parser.add_argument('--test', action='store_true', help='specifies the running mode of DBRL')
#     parser.add_argument('--timesteps', default=10000000, metavar='double', help='specifies the training timesteps. Only works when --train is specified')
#     # parser.add_argument('--modelPath', default=None, metavar='str', help='specifies the pre-trained model. Only works when --train is specified')
#     parser.add_argument('--record', action='store_true', help='specifies whether to record the evaluating result of DBRL. Only works when --test is specified')
#     args = parser.parse_args()
#     return args

# args = parse_args()

env = gym.make(
    "DBRLDf-v0",
    host='192.168.239.1',
    port=50888,
    plane_slot=1,
    enemy_slot=3,
    rendering=False
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

# if args.train:
model.learn(total_timesteps=10000000, log_interval=1)
model.save("./log/sac_df")

# if args.test:
model = SAC.load("./log/sac_df")

win = 0
episode = 0

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
    if dones == True:
        if rewards == 50:
            win += 1
        episode += 1
        time.sleep(2)
        env.reset()
