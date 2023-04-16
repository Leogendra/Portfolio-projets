import pygame
import random
import numpy as np
import agent as agentClass
from display import displayScores
from constantes import *

pygame.init()
font = pygame.font.SysFont('arial', 25)


class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake en apprentissage renforcé')
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                    Point(self.head.x-BLOCK_SIZE, self.head.y),
                    Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 1

        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        

    def play_step(self, action):
        # 1. on regarde si on quite pas la game
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. déplacement de la tête
        self._move(action)
        self.snake.insert(0, self.head)
        
        # 3. check si game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            if self.is_collision():
                reward = NEGATIVE_REWARD
            else:
                reward = NEGATIVE_REWARD
            game_over = True
            return reward, game_over, self.score
        
            
        # 4. on place la pomme
        if self.head == self.food:
            self.frame_iteration = 0
            self.score += 1
            reward = POSITIVE_REWARD
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. mise à jour de l'interface
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. on renvoie le score
        return reward, game_over, self.score
    

    def is_collision(self, point=None):
        if point is None:
            point = self.head
        # on touche un bord
        if point.x > self.w - BLOCK_SIZE or point.x < 0 or point.y > self.h - BLOCK_SIZE or point.y < 0:
            return True
        # on se mord la queue
        if point in self.snake[1:]:
            return True
        
        return False
        

    def _update_ui(self):
        DEMI_BLOCK_SIZE = int(BLOCK_SIZE/2)
        
        self.display.fill(FOND_COLOR)

        is_head = True
        for pt in self.snake:
            pygame.draw.rect(self.display, SNAKE_COLOR_SHADOW, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, SNAKE_COLOR_BODY, pygame.Rect(pt.x+(SHADOW_SIZE/2), pt.y+(SHADOW_SIZE/2), BLOCK_SIZE - SHADOW_SIZE, BLOCK_SIZE - SHADOW_SIZE))
            # petit yeux et langue pour la tête
            if is_head:
                is_head = False
                EYES_SIZE = BLOCK_SIZE/5
                TONGUE_SIZE_LONG = 3*EYES_SIZE/2
                TONGUE_SIZE_LARG = 2*EYES_SIZE/3
                if self.direction == Direction.RIGHT:
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (2*BLOCK_SIZE/3), pt.y + (1*EYES_SIZE), EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (2*BLOCK_SIZE/3), pt.y + (3*EYES_SIZE), EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(pt.x + BLOCK_SIZE, pt.y + (BLOCK_SIZE/2) - 1, TONGUE_SIZE_LONG, TONGUE_SIZE_LARG))
                elif self.direction == Direction.LEFT:
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (1*BLOCK_SIZE/3) - EYES_SIZE, pt.y + (1*EYES_SIZE), EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (1*BLOCK_SIZE/3) - EYES_SIZE, pt.y + (3*EYES_SIZE), EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(pt.x - TONGUE_SIZE_LONG, pt.y + (BLOCK_SIZE/2) - 1, TONGUE_SIZE_LONG, TONGUE_SIZE_LARG))
                elif self.direction == Direction.DOWN:
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (1*EYES_SIZE), pt.y + (2*BLOCK_SIZE/3), EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (3*EYES_SIZE), pt.y + (2*BLOCK_SIZE/3), EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(pt.x + (BLOCK_SIZE/2) - 1, pt.y + BLOCK_SIZE, TONGUE_SIZE_LARG, TONGUE_SIZE_LONG))
                elif self.direction == Direction.UP:
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (1*EYES_SIZE), pt.y + (1*BLOCK_SIZE/3) - EYES_SIZE, EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, SNAKE_COLOR_EYES, pygame.Rect(pt.x + (3*EYES_SIZE), pt.y + (1*BLOCK_SIZE/3) - EYES_SIZE, EYES_SIZE, EYES_SIZE))
                    pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(pt.x + (BLOCK_SIZE/2) - 1, pt.y - TONGUE_SIZE_LONG, TONGUE_SIZE_LARG, TONGUE_SIZE_LONG))


        pygame.draw.circle(self.display, FRUIT_COLOR, [self.food.x + DEMI_BLOCK_SIZE, self.food.y + DEMI_BLOCK_SIZE], DEMI_BLOCK_SIZE)

        textScore = font.render(f"Score : {str(self.score)}", True, TEXT_COLOR)
        self.display.blit(textScore, [0, 0])

        pygame.display.flip()
        

    def _move(self, action):
        # [tout droit, droite, gauche]
        ordre_direction = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = ordre_direction.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):           # on bouge pas
            direction = ordre_direction[index]
        elif np.array_equal(action, [0, 1, 0]):         # on tourne à droite
            direction = ordre_direction[(index+1)%4]
        elif np.array_equal(action, [0, 0, 1]):         # on tourne à gauche
            direction = ordre_direction[(index-1)%4] 

        self.direction = direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)




def trainAgent():
    #Agent
    game = SnakeGame()
    agent = agentClass.Agent()
    getParametres()

    record = 0
    plot_scores = []
    plot_mean_scores = []
    total_score = 0

    while agent.nb_games < NB_TOTAL_GAMES:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, game_over, score = game.play_step(final_move)

        # Entrainement
        state_new = agent.get_state(game)        
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        agent.remember(state_old, final_move, reward, state_new, game_over)
        
        if game_over:
            game.reset()
            agent.nb_games += 1
            agent.train_long_memory()
        
            if score > record:
                record = score
                agent.model.save()
                # print(f"Nouveau record : {record}")
                with open(f"entrainement/{TIME_KEY}.txt", "a") as f:
                    f.write(f"Game:{agent.nb_games};Record:{record}\n")

            if agent.nb_games % 10 == 0:
                agent.model.save()
                # print(f"Game n°{agent.nb_games}, Score : {score}, Record : {record}")

            plot_scores.append(score)

            total_score += score
            mean_score = total_score / agent.nb_games
            
            lissage = 50
            mean_score_glissante = sum(plot_scores[-lissage:]) / min(lissage, agent.nb_games)
            plot_mean_scores.append(mean_score_glissante)
            displayScores(plot_scores, plot_mean_scores, record, glissante=lissage)

    print(f"Game n°{agent.nb_games}, Score : {score}, Record : {record}")
    with open(f"entrainement/{TIME_KEY}.txt", "a") as f:
        f.write(f"moyenne:{mean_score};moyenne_glissante:{mean_score_glissante}\n")



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



if __name__ == "__main__":
    trainAgent()