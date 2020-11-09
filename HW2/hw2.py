# Freddie He
# 1560733
# heyingge

import sys
import time


class Graph(object):
    def __init__(self):
        self.bc = []
        self.ap = set()
        self.nodes = dict()
        self.dfsCounter = 0
        self.dfsNum = dict()
        self.low = dict()
        self.stack = []
        self.rootChildNum = 0

    # a helper function for dfs()
    def dfs_helper(self, v, parent):
        self.dfs(v, parent)

    # recursively explore the graph using DFS
    def dfs(self, v, parent):
        # initialization
        self.dfsCounter += 1
        self.dfsNum[v] = self.dfsCounter
        self.low[v] = self.dfsNum[v]

        for x in self.nodes[v]:
            # x is first time discovered
            if self.dfsNum[x] == -1:
                self.stack.append((v, x))  # first time see this edge, add to edge stack
                self.dfs(x, v)  # recursively find DFS of x
                self.low[v] = min(self.low[v], self.low[x])

                # v is the articulation point splitting x
                if self.low[x] >= self.dfsNum[v]:
                    # if not root, then v is an articulation point
                    if self.dfsNum[v] != 1:
                        self.ap.add(v)
                    self.bc.append([])
                    end = 1
                    # keep popping out edges until find the pair(v, x)
                    while end:
                        edge = self.stack.pop()
                        self.bc[-1].append(edge)
                        if edge == (v, x):
                            end = 0

                # increment the child number
                if self.dfsNum[v] == 1:
                    self.rootChildNum += 1
            elif x != parent:
                self.low[v] = min(self.low[v], self.dfsNum[x])
                if self.dfsNum[v] > self.dfsNum[x] and self.dfsNum[x] != -1:
                    self.stack.append((v, x))  # first time see this edge, add to edge stack

        # check if the root is the articulation point
        if self.rootChildNum > 1:
            self.ap.add(v)


# read vertices and edges
def readfile(filename, gr):
    with open(filename) as f:
        content = f.read().splitlines()
    for line in content:
        vertex = line.split()

        # if is the first time
        if len(vertex) == 1:
            print('There are ' + vertex[0] + ' nodes.')
        else:
            v0 = int(vertex[0])
            v1 = int(vertex[1])

            # fist time see v0
            if v0 not in gr.nodes:
                gr.nodes[v0] = set()
                gr.dfsNum[v0] = -1
                gr.low[v0] = -1
            gr.nodes[v0].add(v1)

            # first time see v1
            if v1 not in gr.nodes:
                gr.nodes[v1] = set()
                gr.dfsNum[v1] = -1
                gr.low[v1] = -1
            gr.nodes[v1].add(v0)
    print('There are ' + str(len(content) - 1) + ' edges.')


def main():
    for filename in sys.argv[1:]:
        gr = Graph()
        readfile(filename, gr)

        # start timing
        start = time.time()
        gr.dfs_helper(gr.nodes.keys()[0], -1)
        end = time.time()

        print('There are ' + str(len(gr.bc)) + ' biconnected components.')
        print('There are ' + str(len(gr.ap)) + ' articulation points.')
        print('Articulation points are ' + str(gr.ap) + '.')
        print('Edges in each biconnected component are ' + str(gr.bc) + '.')
        print('Run time: ' + str(end - start) + "s.")


if __name__ == "__main__":
    main()