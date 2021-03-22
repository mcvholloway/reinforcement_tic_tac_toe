"""
A Minimal Deep Q-Learning Implementation (minDQN)

Running this code will render the agent solving the CartPole environment using OpenAI gym. Our Minimal Deep Q-Network is approximately 150 lines of code. In addition, this implementation uses Tensorflow and Keras and should generally run in less than 15 minutes.

Usage: python3 minDQN.py
"""

import numpy as np
import keras
from keras.models import load_model
from collections import deque
import random
import os
from game import ConnectFourGame
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

rootPath = os.path.dirname(os.path.abspath(__file__))

# """Adding some positional arguments"""
# parser = argparse.ArgumentParser()
# parser.add_argument('--take_existing_model', action='store_true', default='true')
# parser.add_argument('--sequentially_update_opponent', action='store_true', default='true')




# RANDOM_SEED = 5
# tf.random.set_seed(RANDOM_SEED)

# env = gym.make('CartPole-v1')
# env = ConnectFourGame()
# env.seed(RANDOM_SEED)
# np.random.seed(RANDOM_SEED)

# print("Action Space: {}".format(env.action_space))
# print("State space: {}".format(env.board))



def agent(state_shape, action_shape):
    """ The agent maps X-states to Y-actions
    e.g. The neural network output is [.1, .7, .1, .3]
    The highest value 0.7 is the Q-Value.
    The index of the highest action (0.7) is action #1.
    """
    learning_rate = 0.001
    init = keras.initializers.he_uniform()
    model = keras.Sequential()
    model.add(keras.layers.Dense(24, input_shape=[42], activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(12, activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(action_shape, activation='linear', kernel_initializer=init))
    model.compile(loss=keras.losses.Huber(), optimizer=keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])
    return model

def get_qs(model, state, step):
    return model.predict(state.reshape(1, 42))[0]

def train(env, replay_memory, model, target_model, done):
    learning_rate = 0.7 # Learning rate
    discount_factor = 0.618

    MIN_REPLAY_SIZE = 1000
    if len(replay_memory) < MIN_REPLAY_SIZE:
        return

    batch_size = 64 * 2
    mini_batch = random.sample(replay_memory, batch_size)
    current_states = np.array([encode_observation(transition[0], env.board.shape).reshape(42) for transition in mini_batch])
    current_qs_list = model.predict(current_states)
    new_current_states = np.array([encode_observation(transition[3], env.board.shape).reshape(42) for transition in mini_batch])
    future_qs_list = target_model.predict(new_current_states)

    X = []
    Y = []
    for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
        if not done:
            max_future_q = reward + discount_factor * np.max(future_qs_list[index])
        else:
            max_future_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = (1 - learning_rate) * current_qs[action] + learning_rate * max_future_q

        X.append(encode_observation(observation, env.board.shape).reshape(42))
        Y.append(current_qs)
    model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)

def encode_observation(observation, n_dims):
    return observation

def main(use_existing):
    # An episode a full game
    train_episodes = 300
    test_episodes = 100
    env = ConnectFourGame()
    steps_to_update_opponent_threshold = 20000
    epsilon = 1 # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start
    max_epsilon = 1 # You can't explore more than 100% of the time
    min_epsilon = 0.01 # At a minimum, we'll always explore 1% of the time
    decay = 0.01

    # 1. Initialize the Target and Main models
    # Main Model (updated every 4 steps)
    """
    if the take_existing_model flag has been set, try and take an existing model 
    if no such .h5 file exists or if not take_existing_model flag then create a new one
    """
    model = None
    if use_existing:
        for fi in os.listdir(rootPath):
            if '.h5' in fi:
                logging.debug(f'Loading in model {fi} from {rootPath}')
                model = load_model(fi)
                """
                Since an existing connect four model exists go ahead and set the opponent as the existing model
                """
                env = ConnectFourGame(opponent=model)
    elif not model:
        model = agent(env.board.shape, env.n)

    # Target Model (updated every 100 steps)
    target_model = agent(env.board.shape, env.n)
    target_model.set_weights(model.get_weights())

    replay_memory = deque(maxlen=50_000)

    target_update_counter = 0

    # X = states, y = actions
    X = []
    y = []

    steps_to_update_target_model = 0
    # steps_to_update_opponent = 0
    episode = 0
    while True:
        episode += 1
    # for episode in range(train_episodes):
        # total_training_rewards = 0
        observation = env.reset()
        buffer = []
        done = False
        while not done:
            steps_to_update_target_model += 1

            random_number = np.random.rand()
            # 2. Explore using the Epsilon Greedy Exploration Strategy
            if random_number <= epsilon:
                # Explore
                action = random.choice(env.list_valid_actions())
            else:
                # Exploit best known action
                encoded = encode_observation(observation, env.board.shape[0])
                encoded_reshaped = encoded.reshape(1, 42)
                predicted = model.predict(encoded_reshaped).flatten()
                invalid_actions = [x for x in range(7) if x not in env.list_valid_actions()]
                predicted[invalid_actions] = -np.inf
                action = np.argmax(predicted)
            
            new_observation, _ , done, stale_mate = env.step(action)
            buffer.append((observation, action,new_observation))
            
            if len(buffer) > 1:
                if done:
                    while buffer:
                        observation_0, action_0, new_observation_0 = buffer.pop(0)
                        ## This should be -1 unless you are the last player to make a move and it resulted in Victory!
                        reward = -1 + 2*(not stale_mate)*(len(buffer) == 0)
                        replay_memory.append([observation_0, action_0, reward, new_observation_0, done])
                else:
                    observation_0, action_0, new_observation_0 = buffer.pop(0)
                    replay_memory.append([observation_0, action_0, 0, new_observation_0, done])


            # 3. Update the Main Network using the Bellman Equation
            if steps_to_update_target_model % 4 == 0 or done:
                train(env, replay_memory, model, target_model, done)

            observation = new_observation
            # total_training_rewards += reward

            if done:
                if steps_to_update_target_model >= 100:
                    logging.debug('Copying main network weights to the target network weights')
                    target_model.set_weights(model.get_weights())
                    steps_to_update_target_model = 0

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)
        """Every 500 episodes go ahead and save the model"""
        if episode % 500 == 0:
            model.save('connectFourModel.h5')
    model.save('connectFourModel.h5')
    # env.close()

if __name__ == '__main__':
    # args = parser.parse_args()
    # use_existing = True if str(args.take_existing_model).lower() in ['y', 'yes', 'true', 't'] else False
    use_existing = False
    main(use_existing=use_existing)
