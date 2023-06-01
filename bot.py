import Agent

class MineSweeperBot:
    def __init__(self, sizex, sizey):
        self.agent = Agent.Game(sizex, sizey)
        self.queue = []
        self.buffer = []
        self.visited = [[0 for y in range(sizey)] for x in range(sizex)]
        self.sizex = sizex
        self.sizey = sizey

    def reset(self):
        self.agent = Agent.Game(self.sizex, self.sizey)
        self.queue = []
        self.visited = [[0 for y in range(self.sizey)] for x in range(self.sizex)]

    def get_adj(self, x, y):
        adj = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.sizex and 0 <= y + j < self.sizey and (self.agent.opened[x + i][y + j] == 0 or self.agent.opened[x+i][y+j] == 2):
                    adj.append((x + i, y + j))
        return adj

    def get_adj2(self, x, y):
        adj = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.sizex and 0 <= y + j < self.sizey and self.agent.opened[x + i][y + j] == 1:
                    adj.append((x + i, y + j))
        return adj

    def fill_queue(self):
        for y in range(self.sizey):
            for x in range(self.sizex):
                if self.agent.opened[x][y] == 1 and not self.visited[x][y]:
                    self.queue.append((x, y))

    def probability_guess(self):
        prob = [[100000.0 for y in range(self.sizey)] for x in range(self.sizex)]
        for y in range(self.sizey):
            for x in range(self.sizex):
                if self.agent.opened[x][y] == 1 and self.agent.state[x][y] > 0:
                    adj = self.get_adj(x, y)
                    flagged = 0
                    for i in adj:
                        if self.agent.opened[i[0]][i[1]] == 2:
                            flagged += 1
                    if len(adj) == flagged or adj == 0:
                        continue
                    val = self.agent.state[x][y] - flagged
                    for i in adj:
                        if prob[i[0]][i[1]] == 100000:
                            prob[i[0]][i[1]] = 0
                        else:
                            prob[i[0]][i[1]] = max(prob[i[0]][i[1]], val/(len(adj)-flagged) + len(self.get_adj(i[0], i[1]))/2)
        min = 100001
        minx = 0
        miny = 0
        for y in range(self.sizey):
            for x in range(self.sizex):
                if prob[x][y] < min and self.agent.opened[x][y] == 0:
                    min = prob[x][y]
                    minx = x
                    miny = y
        self.agent.open(minx, miny)
        self.queue.append((minx, miny))

    def next_move(self):
        if not self.queue:
            return False

        cur = self.queue[0]
        val = self.agent.state[cur[0]][cur[1]]
        adj = self.get_adj(cur[0], cur[1])
        #print(adj)
        if len(adj) == val:
            for i in adj:
                if self.agent.opened[i[0]][i[1]] == 0:
                    self.agent.flag(i[0], i[1])
                    #print("FLAGGED ", i[0], " ", i[1])
            self.queue.pop(0)
            return True

        flagged = []
        for i in adj:
            if self.agent.opened[i[0]][i[1]] == 2:
                flagged.append(i)
        if len(flagged) == val:
            for i in adj:
                if i in self.buffer:
                    self.buffer = []
                    return False
                if self.agent.opened[i[0]][i[1]] == 0:
                    self.agent.open(i[0], i[1])
                    #print("OPENED ", i[0], " ", i[1])
            self.queue.pop(0)
            self.buffer.append(cur)
            self.visited[cur[0]][cur[1]] = True
            return True
        elif len(flagged) >= val:
            for i in flagged:
                self.agent.flag(i[0], i[1])
                for j in self.get_adj2(i[0], i[1]):
                    self.visited[i[0]][i[1]] = False
            self.queue = []
            return False
            self.agent.gameOver = True
            self.queue.pop(0)
            return False

        self.visited[cur[0]][cur[1]] = False
        self.queue.pop(0)
        return True

    def finish(self):
        for y in range(self.sizey):
            for x in range(self.sizex):
                if self.agent.opened[x][y] == 0:
                    self.agent.open(x, y)
        self.agent.gameOver = True
