import pygame
import numpy as np
import time


class CA:
    def __init__(self, nx_c, ny_c):
        self.nx_c = nx_c
        self.ny_c = ny_c
        self.gameState = np.zeros((nx_c, ny_c))
        self.newGameState = np.copy(self.gameState)

    def apply_rules(self, x, y):
        pass

    def game(self):
        nx_c = self.nx_c
        ny_c = self.ny_c

        pygame.init()

        width, height = 1000, 1000
        screen = pygame.display.set_mode((height, width))

        bg = 255, 255, 255

        screen.fill(bg)

        dim_cw = width / nx_c
        dim_ch = height / ny_c

        pauseExect = False

        # Execution loop
        while True:

            self.newGameState = np.copy(self.gameState)

            screen.fill(bg)

            time.sleep(0.01)

            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.KEYDOWN:
                    pauseExect = not pauseExect

                mouseClick = pygame.mouse.get_pressed()

                if sum(mouseClick) > 0:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    cel_x, cel_y = int(np.floor(pos_x / dim_cw)), int(np.floor(pos_y / dim_ch))
                    self.newGameState[cel_x, cel_y] = not mouseClick[2]

            for y in range(ny_c):

                for x in range(nx_c):

                    if not pauseExect:
                        self.apply_rules(x, y)

                    poly = [((x) * dim_cw, (y) * dim_ch),
                            ((x + 1) * dim_cw, (y) * dim_ch),
                            ((x + 1) * dim_cw, (y + 1) * dim_ch),
                            ((x) * dim_cw, (y + 1) * dim_ch)]

                    if self.newGameState[x, y] == 0:
                        pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                    else:
                        pygame.draw.polygon(screen, (25, 25, 25), poly, 0)

            self.gameState = np.copy(self.newGameState)

            pygame.display.flip()


class GOL(CA):
    def apply_rules(self, x, y):
        nx_c = self.nx_c
        ny_c = self.ny_c

        n_neigh = self.gameState[(x + 1) % nx_c, (y + 1) % ny_c] + \
                  self.gameState[(x + 1) % nx_c, (y) % ny_c] + \
                  self.gameState[(x + 1) % nx_c, (y - 1) % ny_c] + \
                  self.gameState[(x) % nx_c, (y + 1) % ny_c] + \
                  self.gameState[(x) % nx_c, (y - 1) % ny_c] + \
                  self.gameState[(x - 1) % nx_c, (y + 1) % ny_c] + \
                  self.gameState[(x - 1) % nx_c, (y) % ny_c] + \
                  self.gameState[(x - 1) % nx_c, (y - 1) % ny_c]

        # Rule 1: if a dead cell has exactly 3 neighbour cells, it comes to life
        if self.gameState[x, y] == 0 and n_neigh == 3:
            self.newGameState[x, y] = 1

        # Rule 2: if a live cell has 2 or 3 neighbour cells alive it continues alive, otherwise it dies
        elif self.gameState[x, y] == 1 and not (n_neigh == 2 or n_neigh == 3):
            self.newGameState[x, y] = 0


class RuleX(CA):
    def set_rule(self, rule):
        rule_bin = []
        
        # transform from base10 to base2
        while not (rule == 1 or rule == 0):
            p = rule // 2
            q = rule % 2

            rule_bin.append(q)

            rule = p
            if rule == 1:
                rule_bin.append(1)

        for i in range(8 - len(rule_bin)):
            rule_bin.append(0)

        self.rule_bin = rule_bin

    def apply_rules(self, x, y):
        nx_c = self.nx_c
        ny_c = self.ny_c
        rule_bin = self.rule_bin

        if x == nx_c // 2 and y == 0:
            self.newGameState[x, y] = 1

        if y == 0 or x == 0 or x == nx_c - 1:
            return

        neigh = [self.gameState[(x - 1), (y - 1)],
                 self.gameState[(x), (y - 1)],
                 self.gameState[(x + 1), (y - 1)]]

        if neigh[0] == 0 and neigh[1] == 0 and neigh[2] == 0:
            self.newGameState[x, y] = rule_bin[0]
        elif neigh[0] == 0 and neigh[1] == 0 and neigh[2] == 1:
            self.newGameState[x, y] = rule_bin[1]
        elif neigh[0] == 0 and neigh[1] == 1 and neigh[2] == 0:
            self.newGameState[x, y] = rule_bin[2]
        elif neigh[0] == 0 and neigh[1] == 1 and neigh[2] == 1:
            self.newGameState[x, y] = rule_bin[3]
        elif neigh[0] == 1 and neigh[1] == 0 and neigh[2] == 0:
            self.newGameState[x, y] = rule_bin[4]
        elif neigh[0] == 1 and neigh[1] == 0 and neigh[2] == 1:
            self.newGameState[x, y] = rule_bin[5]
        elif neigh[0] == 1 and neigh[1] == 1 and neigh[2] == 0:
            self.newGameState[x, y] = rule_bin[6]
        elif neigh[0] == 1 and neigh[1] == 1 and neigh[2] == 1:
            self.newGameState[x, y] = rule_bin[7]
