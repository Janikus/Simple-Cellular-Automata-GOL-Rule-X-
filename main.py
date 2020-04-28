import pygame
import numpy as np
import time
import random


class CA:
    def __init__(self, nx_c, ny_c):
        self.nx_c = nx_c
        self.ny_c = ny_c
        self.gameState = np.zeros((nx_c, ny_c))
        self.newGameState = np.copy(self.gameState)
        self.time_step = 0.01
        self.iteration = 0

    def apply_rules(self, x, y):
        pass

    def get_range(self):
        return range(0, self.ny_c)

    def change_time_step(self, time_step):
        self.time_step = time_step

    def game(self):
        nx_c = self.nx_c
        ny_c = self.ny_c

        pygame.init()

        width, height = int(nx_c * (1000 / ny_c)), 1000
        screen = pygame.display.set_mode((width, height))

        bg = 255, 255, 255

        # screen.fill(bg)

        dim_cw = width / nx_c
        dim_ch = height / ny_c

        pause_except = False

        # Execution loop
        while True:

            self.newGameState = np.copy(self.gameState)

            # screen.fill(bg)

            time.sleep(self.time_step)

            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        middle_column(self.gameState, self.nx_c)
                    else:
                        pause_except = not pause_except

                mouse_click = pygame.mouse.get_pressed()

                if sum(mouse_click) > 0:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    cel_x, cel_y = int(np.floor(pos_x / dim_cw)), int(np.floor(pos_y / dim_ch))
                    self.newGameState[cel_x, cel_y] = not mouse_click[2]

            y_range = self.get_range()

            for y in y_range:

                for x in range(nx_c):

                    if not pause_except:
                        self.apply_rules(x, y)

            for y in range(ny_c):

                for x in range(nx_c):

                    poly = [((x) * dim_cw, (y) * dim_ch),
                            ((x + 1) * dim_cw, (y) * dim_ch),
                            ((x + 1) * dim_cw, (y + 1) * dim_ch),
                            ((x) * dim_cw, (y + 1) * dim_ch)]

                    if self.newGameState[x, y] == 0:
                        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)  # white
                    else:
                        pygame.draw.polygon(screen, (25, 25, 25), poly, 0)  # black

            self.gameState = np.copy(self.newGameState)
            self.iteration += 1

            '''starting = 0
            new_rule = 0
            for y in y_range:
                for x in range(nx_c):
                    if self.gameState[x, y] == 1:
                        starting = x
                        break
                if starting != 0:
                    for i in range(starting, starting + 8):
                        if self.gameState[i, y] == 1:
                            new_rule += (2 ** (i - starting))

            for i in range(starting, starting + 8):
                if self.gameState[i, y_range] == 1:
                    new_rule += (2 ** (i - starting))

            self.set_rule(new_rule)'''

            # self.set_rule(self.iteration)

            pygame.display.flip()

    def set_rule(self, new_rule):
        pass


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

        '''if y == 0:
            self.newGameState[x, y] = random.randint(0, 1)'''

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

    def get_range(self):
        if self.iteration == self.ny_c:
            self.iteration -= 1
        return range(self.iteration, self.iteration + 1)


class MultX(CA):
    def set_step(self, step):
        self.step = step

    def apply_rules(self, x, y):
        if y == 0:
            if x == self.nx_c - 1:
                self.newGameState[x, y] = 1
            else:
                self.newGameState[x, y] = 0
            return

        next_step = []
        last = 0

        for i in range(self.nx_c):
            last += (2 ** (self.nx_c - 1 - i)) * self.gameState[i, y - 1]

        print(last)

        sum = last * self.step
        # transform from base10 to base2
        while not (sum == 1 or sum == 0):
            p = sum // 2
            q = sum % 2

            next_step.append(q)

            sum = p
            if sum == 1:
                next_step.append(1)

        for i in range(self.nx_c - len(next_step)):
            next_step.append(0)

        next_step.reverse()

        self.newGameState[x, y] = next_step[x]

    def get_range(self):
        if self.iteration == self.ny_c:
            self.iteration -= 1
        return range(self.iteration, self.iteration + 1)


class CodeX(CA):
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

        if self.iteration == 0 and y == self.ny_c // 2 and x == self.nx_c // 2:
            self.newGameState[x, y] = 1
            return

        neigh = [self.gameState[(x) % nx_c, (y - 1) % ny_c],
                 self.gameState[(x - 1) % nx_c, (y) % ny_c],
                 self.gameState[(x + 1) % nx_c, (y) % ny_c],
                 self.gameState[(x) % nx_c, (y + 1) % ny_c]]

        # Count number of black cells in neighbours
        n_black = 0
        for n in neigh:
            if n == 1:
                n_black += 1

        if self.gameState[x, y] == 0 and n_black == 0:
            self.newGameState[x, y] = rule_bin[0]
        elif self.gameState[x, y] == 1 and n_black == 0:
            self.newGameState[x, y] = rule_bin[1]
        else:
            self.newGameState[x, y] = rule_bin[n_black + 1]


def middle_column(gameState, nx_c):
    print("saved")
    file = open("middle_column.txt", "w")
    col = gameState[nx_c // 2]
    for i in col:
        file.write(str(int(i)))
    file.close()
