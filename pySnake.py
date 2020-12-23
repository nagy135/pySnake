import pygame
import time
import random

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)
blue = (0, 0, 255)

WIDTH = 1000
HEIGHT = 1000

INIT_FOOD = [ 10,10 ]

TICK_TIME = .02
SPAWN_FOOD_TIME = 10

BRICK_SIZE = 20

FOOD_SIZE = 20

INIT_POSITIONS = [
            (20,20),
            (21,20),
            (22,20),
            (22,21),
            (22,22),
            (22,23),
        ]

class pySnake:

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('pySnake')
        self.time = time.time()
        self.food_time = time.time()
        self.clock = pygame.time.Clock()

        self.body = INIT_POSITIONS
        self.direction = (0, 1)
        self.lenghten = False

        self.food = INIT_FOOD

        self.impossible_moves = {
                'up': (0,1),
                'left': (1,0),
                'down': (0,-1),
                'right': (-1,0),
                }



    def player_move(self, direction):
        if self.impossible_moves[direction] == self.direction:
            return False
        if direction == 'up':
            self.direction = (0, -1)
        elif direction == 'left':
            self.direction = (-1, 0)
        elif direction == 'down':
            self.direction = (0, 1)
        elif direction == 'right':
            self.direction = (1, 0)


    def board_to_pixels(self, cell):
        return (cell[0] * BRICK_SIZE, cell[1] * BRICK_SIZE)

    def draw(self):
        for cell in self.body:
            cell = self.board_to_pixels(cell)
            pygame.draw.rect(self.gameDisplay, red, (cell[0], cell[1], BRICK_SIZE, BRICK_SIZE))

        food = self.board_to_pixels(self.food)
        pygame.draw.rect(self.gameDisplay, green, (food[0], food[1], FOOD_SIZE, FOOD_SIZE))


    def move_cell_direction(self, cell):
        return (cell[0] + self.direction[0], cell[1] + self.direction[1])

    def move(self):
        actual_time = time.time()
        if actual_time - self.time > TICK_TIME:
            self.time = actual_time
        else:
            return

        if not self.lenghten:
            self.body.pop(0)
        else:
            self.lenghten = not self.lenghten

        new_block = self.move_cell_direction(self.body[-1])
        if self.hit_wall(new_block) or self.hit_self():
            self.end = True
            return
        self.body.append(new_block)

        if self.body[-1][0] == self.food[0] and self.body[-1][1] == self.food[1]:
            self.food[0] = random.randint(0, WIDTH / BRICK_SIZE)
            self.food[1] = random.randint(0, HEIGHT / BRICK_SIZE)

            self.lenghten = True


        food_time_new = time.time()
        if food_time_new - self.time > SPAWN_FOOD_TIME:
            self.food_time = food_time_new
        else:
            return

        self.food[0] = random.randint(0, WIDTH / BRICK_SIZE)
        self.food[1] = random.randint(0, HEIGHT / BRICK_SIZE)

    
    def hit_self(self):
        for cell in self.body[:-1]:
            if cell == self.body[-1]:
                return True
        return False



    def hit_wall(self, cell):
        if cell[0] < 0 or cell [1] < 0:
            return True
        if cell[0] > (WIDTH / BRICK_SIZE) or cell[1] > (HEIGHT / BRICK_SIZE):
            return True
        return False

    def start(self):
        self.end = False
        while not self.end:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player_move('up')
                    if event.key == pygame.K_a:
                        self.player_move('left')
                    if event.key == pygame.K_s:
                        self.player_move('down')
                    if event.key == pygame.K_d:
                        self.player_move('right')
                    if event.key == pygame.K_r:
                        self.__init__()
                    if event.key == pygame.K_q:
                        self.end = True
                if event.type == pygame.QUIT:
                    self.end = True
            self.gameDisplay.fill(white)
            self.move()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

a = pySnake()
a.start()
