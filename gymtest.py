import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

env = gym.make('CartPole-v0')
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

# creating the model

model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

# applying keras model to reinforcement learning algorithm

policy = EpsGreedyQPolicy()
memory = SequentialMemory(limit=50000, window_length=1)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory,nb_steps_warmup=10, target_model_update=1e-2,policy=policy)
dqn.compile(Adam(lr=1e-3),metrics=['mae'])

# fitting the reinforcement learning algorithm to the game environment
dqn.fit(env,nb_steps=5000, visualize=True, verbose=2)