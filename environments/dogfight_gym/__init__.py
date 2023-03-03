# try:
#     from src.environments.dogfightEnv.dogfightEnv import DogfightEnv
# except:
#     from gym.envs.dogfightEnv.dogfightEnv import DogfightEnv

from gym.envs.registration import register

from .dogfight_env import DogfightEnv

environments = [['DogfightEnv', 'v0']]

for environment in environments:
    register(
        id='{}-{}'.format(environment[0], environment[1]),
        entry_point='environments.dogfight_gym.dogfight_env:{}'.format(environment[0]),
        nondeterministic=True
    )


__all__ = ["DogfightEnv"]


