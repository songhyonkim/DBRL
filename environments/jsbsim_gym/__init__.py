# try:
#     from src.environments.jsbsimEnv.jsbsimEnv import JsbsimEnv
#     from src.environments.jsbsimEnv.jsbsimFdm import JsbsimFdm
# except:
#     from gym.envs.jsbsimEnv.jsbsimEnv import JsbsimEnv
#     from gym.envs.jsbsimEnv.jsbsimFdm import JsbsimFdm

from gym.envs.registration import register

from .jsbsim_env import JsbsimEnv

environments = [['JsbsimEnv', 'v0']]

for environment in environments:
    register(
        id='{}-{}'.format(environment[0], environment[1]),
        entry_point='environments.jsbsim_gym.jsbsim_env:{}'.format(environment[0]),
        nondeterministic=True
    )


__all__ = ["JsbsimEnv"]


