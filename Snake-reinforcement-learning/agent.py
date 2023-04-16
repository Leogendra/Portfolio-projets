import random
import numpy as np
import torch
from collections import deque
from model import Linear_QNet, QTrainer
from constantes import *

class Agent:
    def __init__(self):
        getParametres()
        self.nb_games = 0
        self.epsilon = 0                     # seed du random
        self.gamma = GAMMA_DISCOUNT_RATE     # discount rate < 1, poids que met l'agent sur les reward passés
        self.memory = deque(maxlen=MAX_MEMORY)  # tas.  si max memoire dépassé -> popleft()
        self.model = Linear_QNet(11, HIDDEN_SIZE, 3)
        self.trainer = QTrainer(self.model, learning_rate=VITESSE_APPRENTISSAGE, gamma=self.gamma)


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger en face
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger à droite
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger à gauche
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food direction 
            game.food.x < game.head.x,  # food gauche
            game.food.x > game.head.x,  # food droite
            game.food.y < game.head.y,  # food haut
            game.food.y > game.head.y  # food bas
        ]

        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def train_long_memory(self):
        mini_sample = 0
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # liste de 1000 tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


    def get_action(self, state):
        # déplacement aléatoire, ou déplacement selon le modèle
        self.epsilon = EPSILON_NB_GAMES - self.nb_games
        next_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            next_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            next_move[move] = 1

        return next_move
    



def getParametres():
    global TIME_KEY, GAMMA_DISCOUNT_RATE, VITESSE_APPRENTISSAGE, EPSILON_NB_GAMES, HIDDEN_SIZE, NB_TOTAL_GAMES

    if os.path.exists("entrainement/parametres.txt"):
        params = [line for line in open("entrainement/parametres.txt", "r")]

        TIME_KEY = params[0].strip()
        GAMMA_DISCOUNT_RATE = float(params[1].strip())
        VITESSE_APPRENTISSAGE = float(params[2].strip())
        EPSILON_NB_GAMES = int(params[3].strip())
        HIDDEN_SIZE = int(params[4].strip())
        NB_TOTAL_GAMES = int(params[5].strip())