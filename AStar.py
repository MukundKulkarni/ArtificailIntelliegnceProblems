import sys, pygame
import random
from pygame.locals import *

white = (219, 217, 217)
blue = (157, 214, 250)
green = (128, 237, 159)
red = (247, 69, 69)
yellow = (252, 187, 66)
black = (0, 0, 0)
gray = (145, 145, 145)


class Node:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.previous = None
        self.wall = False

    def addNeighbours(self, grid):
        i = self.x
        j = self.y

        if (i < cols - 1):
            self.neighbours.append(grid[i+1][j])

        if (i > 0):
            self.neighbours.append(grid[i-1][j])

        if (j < rows - 1):
            self.neighbours.append(grid[i][j+1])

        if (j > 0):
            self.neighbours.append(grid[i][j-1])

        if (i > 0 and j > 0):
            self.neighbours.append(grid[i-1][j-1])

        if (i < cols - 1 and j > 0):
            self.neighbours.append(grid[i+1][j-1])

        if (i > 0 and j < rows - 1):
            self.neighbours.append(grid[i-1][j+1])

        if (i < cols-1 and j < rows-1):
            self.neighbours.append(grid[i+1][j+1])



pygame.init()
clock = pygame.time.Clock()

cols, rows = 30, 30

grid = [[Node(i, j) for j in range(cols) ]for i in range(rows)] # Graph for the A* Search

for i in range(rows):
    for j in range(cols):
        wall = random.randint(0, 2)
        if wall == 1:
            grid[i][j].wall = True
        grid[i][j].addNeighbours(grid)

closed_set = [] #Nodes we have evaluated
open_set = [] #Nodes we havent evaluated


start = grid[0][0]
end = grid[cols-1][rows-1]

start.wall = False
end.wall = False

open_set.append(start)

#print(grid)

length = 20
breadth = 20
margin = 5

size = width, height = ((length + margin)* cols + margin ) , ((breadth + margin)* rows + margin)


def updateClosedSet(closed_set):
    for node in closed_set:
        pygame.draw.rect(window, red,((margin + length) * node.y + margin, (margin + breadth) * node.x + margin, length, breadth))
        pygame.display.update()

def updateOpenSet(closed_set):
    for node in open_set:
        pygame.draw.rect(window, green,((margin + length) * node.y + margin, (margin + breadth) * node.x + margin, length, breadth))
        pygame.display.update()

def drawGrid(rows, cols):
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].wall == True:
                pygame.draw.rect(window, gray,((margin + length) * j + margin, (margin + breadth) * i + margin, length, breadth))
            else:
                pygame.draw.rect(window, white,((margin + length) * j + margin, (margin + breadth) * i + margin, length, breadth))

    pygame.display.update()

def heuristic(a, b):
    # The Heuristic takes the Euclidian Distance to find the next best node
    dist = (a.x - b.x)**2 + (a.y - b.y)**2
    return dist

def drawPath(path):
    for node in path:
        pygame.draw.rect(window, yellow,((margin + length) * node.y + margin, (margin + breadth) * node.x + margin, length, breadth))
        pygame.display.update()
        msElapsed = clock.tick(10)


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


window = pygame.display.set_mode(size)
pygame.display.set_caption("Window")

found_path = False
path = []

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    drawGrid(rows, cols)

    # THE A* A LGORITHM

    while not found_path:

        if len(open_set) > 0:
            # We can continue, so we check if any of the nodes in the open_set
            # has a lower value of f (distance from the end) than the present value

            curr_lowest_index = 0

            for i, node in enumerate(open_set):
                if node.f < open_set[curr_lowest_index].f:
                    curr_lowest_index = i

            curr = open_set[curr_lowest_index]

            neighbours = curr.neighbours


            for neighbour in neighbours:
                if neighbour in closed_set or neighbour.wall:
                    continue

                if neighbour in open_set:
                    neighbour.g = min(neighbour.g, curr.g + 1)
                    new_path = True
                else:
                    neighbour.g = curr.g + 1
                    open_set.append(neighbour)

                neighbour.h = heuristic(neighbour, end)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.previous = curr

            if curr == end:
                temp = end
                path.append(temp)
                while(temp.previous != None):
                    path.append(temp.previous)
                    temp = temp.previous
                print("Done!")
                found_path = True
                drawPath(path)
                wait()
            else:
                updateOpenSet(open_set)
                updateClosedSet(closed_set)
                closed_set.append(curr)
                open_set.remove(curr)

        else:
            #We have no solution
            print("No Solution!!!")
            wait()

        msElapsed = clock.tick(5)
