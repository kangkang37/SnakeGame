

import pygame
from collections import deque
import numpy as np
import random
import os

pygame.init()

music_path = './snakeMusic.mp3'
# music_path = './your_music_path.mp3'
bgm = False # whether to play the background music
if os.path.exists(music_path):
    bgm = True
    pygame.mixer.music.load(music_path)


# size of screen
# WINDOW_WIDTH, WINDOW_HEIGHT = 240,240
WINDOW_WIDTH, WINDOW_HEIGHT = 320,240 # width-- Y  height-- X
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


clock = pygame.time.Clock()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255, 255, 255)
GRAY = (128,128,128)
YELLOW = (255,255,0)
BROWNYELLOW=(153,76,0)
ORANGE=(255,99,71)

Threshold=0.8 # use longest path if the body area > total area*0.8

# size of grid
GRID_SIZE = 20 # original 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

game_state = "start"  # 可以为 "start", "running", "paused"

score = 0

font = pygame.font.Font(None, 24)

dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]

class Snake:
    def __init__(self):
        # self.body = [(5, 5), (5, 6), (5, 7)]
        self.body=[(2,2),(2,3),(2,4)]
        self.direction = 'UP'

    def move(self, direction):
        self.tail = self.body[-1]
        if direction == 'UP':
            self.body.insert(0, (self.body[0][0]-1, self.body[0][1] ))
        if direction == 'DOWN':
            self.body.insert(0, (self.body[0][0]+1, self.body[0][1] ))
        if direction == 'LEFT':
            self.body.insert(0, (self.body[0][0] , self.body[0][1]-1))
        if direction == 'RIGHT':
            self.body.insert(0, (self.body[0][0] , self.body[0][1]+1))
        self.body.pop()

    def grow(self):
        self.body.append(self.tail)

    def copy(self):
        snake_copy=Snake()
        snake_copy.body=self.body
        snake_copy.direction=self.direction
        return snake_copy

class Food:
    def __init__(self):
        self.position = [1,1]

    def respawn(self):
        self.position = [np.random.randint(0, GRID_HEIGHT), np.random.randint(0, GRID_WIDTH)]


      
snake = Snake()

food = Food()

# Path finding function
# The shortest path from the snake's head to the food is found through the breadth-first search algorithm.
def find_shortest_path(snake, food):
    fx,fy=food[0],food[1]

    queue = deque()
    queue.append(snake.body[0])

    # Create an empty 2D list to save the state of each cell
    # 0 indicates unvisited
    # 1 indicates the snake's body
    # 2 indicates already visited
    state = [[0]*GRID_WIDTH for _ in range(GRID_HEIGHT)] ###
    for pos in snake.body:
        state[pos[0]][pos[1]] = 1
    state[fx][fy] = 0

    # Create an empty 2D list to store the distance of each cell
    dist = [[-1]*GRID_WIDTH for _ in range(GRID_HEIGHT)] ###
    dist[snake.body[0][0]][snake.body[0][1]] = 0

    # Create an empty 2D list to store the direction of each cell
    prev = [[(-1, -1)]*GRID_WIDTH for _ in range(GRID_HEIGHT)] ###

    containFood=False
    path=[]
    curr_direc=snake.direction
    while queue:
        # if containFood:
        #     break
        x, y = queue.popleft()
        
        if (x,y)==food:
            while not (x == snake.body[0][0] and y == snake.body[0][1]):
                path.append((x, y))
                x, y = prev[x][y]
            path.reverse()
            return path
        
        # dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        # random.shuffle(dirs)

        # try to keep straight
        if (x,y)==snake.body[0]:
            curr_direc=snake.direction
        else:
            parent=prev[x][y]
            curr_direc=getDirection(parent,(x,y))
        if curr_direc=="UP":
            idx=dirs.index((-1,0))
            dirs[idx],dirs[0]=dirs[0],dirs[idx]
        elif curr_direc=="DOWN":
            idx=dirs.index((1,0))
            dirs[idx],dirs[0]=dirs[0],dirs[idx]
        elif curr_direc=="LEFT":
            idx=dirs.index((0,-1))
            dirs[idx],dirs[0]=dirs[0],dirs[idx]
        else:
            idx=dirs.index((0,1))
            dirs[idx],dirs[0]=dirs[0],dirs[idx]

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy

            if nx < 0 or ny < 0 or nx >= GRID_HEIGHT or ny >= GRID_WIDTH or state[nx][ny] !=0:
                continue

            if state[nx][ny] == 0:
                queue.append((nx, ny))
                state[nx][ny] = 2
                dist[nx][ny] = dist[x][y] + 1
                prev[nx][ny] = (x, y)
                # if (nx,ny)==tuple([fx,fy]):
                #     containFood=True
                #     break

    # # Path backtracking
    # path = []
    # if containFood==False:
    #     return []
    # x, y = fx, fy
    # while not (x == snake.body[0][0] and y == snake.body[0][1]):
    #     path.append((x, y))
    #     x, y = prev[x][y]
    # path.reverse()

    return path


def find_longest_path(snake,dst):
    path=find_shortest_path(snake,dst)
    # print('in longest, path',path)

    if path==[]:
        return []

    state = [[0]*GRID_WIDTH for _ in range(GRID_HEIGHT)]
    for pos in snake.body:
        state[pos[0]][pos[1]] = 1
    for pos in path:
        state[pos[0]][pos[1]]=2

    extension=False

    # if i can find the shortest path
    idx=0
    while True:
        extension=False
        # print('while path',path)

        nx_point=path[idx]
        curr_point=tuple()
        if idx==0:
            curr_point=snake.body[idx]
        else:
            curr_point=path[idx-1]
        direc=getDirection(curr_point,nx_point)
        # print('direc',direc)

        temp_nx_direc=[]
        if direc=='UP' or direc=='DOWN':
            temp_nx_direc=['LEFT','RIGHT']
            random.shuffle(temp_nx_direc)
        if direc=='LEFT' or direc=='RIGHT':
            temp_nx_direc=['UP',"DOWN"]
            random.shuffle(temp_nx_direc)
        for tempDir in temp_nx_direc:
            temp_nx_point=getAdjacent(nx_point,tempDir)
            temp_curr_point=getAdjacent(curr_point,tempDir)
        
            if inMap(temp_nx_point) and inMap(temp_curr_point) and state[temp_curr_point[0]][temp_curr_point[1]]==0 and state[temp_nx_point[0]][temp_nx_point[1]]==0:
                path.insert(idx,temp_curr_point)
                path.insert(idx+1,temp_nx_point)
                state[temp_curr_point[0]][temp_curr_point[1]]=2
                state[temp_nx_point[0]][temp_nx_point[1]]=2
                extension=True
                break
                
        if extension==False:
            idx+=1
            if idx>=len(path):
                break
    return path





def getDirection(src,des): # the direction from source to destination
    x,y=src[0],src[1]
    nx,ny=des[0],des[1]
    direc=None
    if x==nx:
        if y==(ny+1):
            direc='LEFT'
        elif y==(ny-1):
            direc='RIGHT'
    elif x==(nx-1) and y==ny:
        direc="DOWN"
    elif x==(nx+1) and y==ny:
        direc="UP"
    return direc

def getAdjacent(src,direc):
    x,y=src[0],src[1]
    if direc=='UP':
        return tuple([x-1,y])
    if direc=='DOWN':
        return tuple([x+1,y])
    if direc=='LEFT':
        return tuple([x,y-1])
    if direc=="RIGHT":
        return tuple([x,y+1])


def getAllAdjacents(snake):
    # find all adj from snake head
    head=snake.body[0]
    ans=[]
    for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
        nx=(head[0]+dx,head[1]+dy)
        if nx not in snake.body:
            ans.append(nx)
    return ans

def inMap(node):
    x,y=node[0],node[1]
    if x>=0 and y>=0 and x<GRID_HEIGHT and y<GRID_WIDTH:
        return True
    return False

def isValidPoint(adj,snake,food):
    if adj[0]==food.position[0] and adj[1]==food.position[1]:
        if adj not in snake.body:
            return True
    if adj not in snake.body[:-1]:
        return True
    return False

def manhattanDistance(src,food):
    fx,fy=food.position[0],food.position[1]
    x,y=src[0],src[1]
    return abs(x-fx)+abs(y-fy)

def isEndlessLoop(snake):
    # the endless loop is: head adjacent to tail and the emptycells are single.
    hx,hy=snake.body[0][0],snake.body[0][1]
    tx,ty=snake.body[-1][0],snake.body[-1][1]
    ans=True
    if (hx==tx and abs(hy-ty)==1) or (hy==ty and abs(hx-tx)==1): # adj
        map=[(x,y) for x in range(GRID_HEIGHT) for y in range(GRID_WIDTH)]
        for k in map:
            if k not in snake.body:
                temp=0
                for (dx,dy) in dirs:
                    adj_k=(dx+k[0],dy+k[1])
                    if inMap(adj_k) and adj_k in snake.body:
                        temp+=1
                if temp<4: # is single empty cell
                    ans=False
                    break
    else:
        ans=False
    return ans



def main():
    global game_state, snake, food, score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if game_state == "start" and start_button.collidepoint(mouse_pos):
                    if bgm: pygame.mixer.music.play(-1)
                    # pygame.mixer.music.stop()
                    game_state = "running"
                elif game_state == "running" and stop_button.collidepoint(mouse_pos):
                    if bgm: pygame.mixer.music.pause()
                    game_state = "paused"
                elif game_state == "paused" and start_button.collidepoint(mouse_pos):
                    if bgm: pygame.mixer.music.unpause()
                    game_state = "running"

        # Game start screen
        # Note: In pygame, the X-axis extends to the right, the Y-axis extends downward, and the origin is at the top-left corner.
        if game_state == "start":
            # window.fill(BLACK)
            # pygame.mixer.music.play(-1)
            if bgm: pygame.mixer.music.stop()
            start_button = pygame.draw.rect(window, ORANGE, (WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT//2 - 20, 100, 40))
            window.blit(font.render('START', True, BLACK), (WINDOW_WIDTH//2 - 24, WINDOW_HEIGHT//2 - 6))
            pygame.display.update()
            continue

        # Game pause screen
        if game_state == "paused":
            # window.fill(BLACK)
            # start_button = pygame.draw.rect(window, GREEN, (WINDOW_WIDTH//2 - 50, WINDOW_HEIGHT//2 - 20, 100, 40))

            start_button = pygame.draw.rect(window, YELLOW, (WINDOW_WIDTH - 60, 10, 50, 25))

            window.blit(font.render('start', True, BROWNYELLOW), (WINDOW_WIDTH - 53, 15))

            # window.blit(font.render('Start', True, WHITE), (WINDOW_WIDTH//2 - 30, WINDOW_HEIGHT//2 - 15))
            pygame.display.update()
            continue

        # game running
        if game_state == "running":
            window.fill(BLACK)

            # draw snake head and body and tail
            # pygame.draw.rect(window, GREEN, (snake.body[0][0]*GRID_SIZE, snake.body[0][1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            # pygame.draw.circle(window, GREEN, (snake.body[0][0]*GRID_SIZE + GRID_SIZE//2, snake.body[0][1]*GRID_SIZE + GRID_SIZE//2), GRID_SIZE//2)
            pygame.draw.circle(window, GREEN, (snake.body[0][1]*GRID_SIZE + GRID_SIZE//2, snake.body[0][0]*GRID_SIZE + GRID_SIZE//2), GRID_SIZE//2)

            for pos in snake.body[1:-1]:
                # pygame.draw.rect(window, WHITE, (pos[0]*GRID_SIZE, pos[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.circle(window, WHITE, (pos[1]*GRID_SIZE + GRID_SIZE//2, pos[0]*GRID_SIZE + GRID_SIZE//2), GRID_SIZE//2)

            pygame.draw.circle(window, GRAY, (snake.body[-1][1]*GRID_SIZE + GRID_SIZE//2, snake.body[-1][0]*GRID_SIZE + GRID_SIZE//2), GRID_SIZE//2)

            # show the score
            window.blit(font.render('Score: {}'.format(score), True, ORANGE), (10, 10))

            # show the pause button
            stop_button = pygame.draw.rect(window, YELLOW, (WINDOW_WIDTH - 60, 10, 50, 25)) # (WINDOW_WIDTH - 60, 10, 50, 30)
            window.blit(font.render('stop', True, BROWNYELLOW), (WINDOW_WIDTH - 52, 15))

            # draw food
            pygame.draw.rect(window, RED, (food.position[1]*GRID_SIZE, food.position[0]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # new algorithm

            def findDirection(snake,food):
                snake_copy=Snake()
                snake_copy.body=snake.body.copy()
                snake_copy.direction=snake.direction

                # snake_copy=snake.body.copy() # if here is snake.copy(), change snake_copy, the snake will change too
                short_path=find_shortest_path(snake,(food.position[0],food.position[1]))
                if short_path:
                    if isEndlessLoop(snake):
                        nx_point=short_path[0]
                        return getDirection(snake.body[0],nx_point)
                    # print('short',short_path)
                    curr=snake_copy.body[0]
                    # print(curr)
                    for i in range(len(short_path)):
                        nx_point=short_path[i]
                        direc=getDirection(curr,nx_point)
                        snake_copy.move(direc)
                        curr=nx_point
                        if nx_point[0]==food.position[0] and nx_point[1]==food.position[1]:
                            snake_copy.grow()
                    # print(snake_copy.body)
                    if len(snake_copy.body)>=(GRID_HEIGHT*GRID_WIDTH-1): # is filled
                        nx_point=short_path[0]
                        return getDirection(snake.body[0],nx_point)

                    # step 3
                    # get the longest path to tail
                    longest_path_to_tail=find_longest_path(snake_copy,snake_copy.body[-1])

                    # # If the snake is too long, take the longest path to the food. This method may fall into an infinite loop.
                    # if len(longest_path_to_tail)>1 and len(snake_copy.body)<Threshold*GRID_HEIGHT*GRID_WIDTH:
                    #     nx_point=short_path[0]
                    #     direc=getDirection(snake.body[0],nx_point)
                    #     return direc

                    if len(longest_path_to_tail)>=1: #orig >1
                        nx_point=short_path[0]
                        direc=getDirection(snake.body[0],nx_point)
                        return direc

                # can't find the shortest path
                path_to_tail=find_longest_path(snake,snake.body[-1])
                # if len(path_to_tail)>=1: # orig >1
                #     nx_point=path_to_tail[0]
                #     return getDirection(snake.body[0],nx_point)

                if len(path_to_tail)>=1: # orig >1
                    nx_point=path_to_tail[0]
                    return getDirection(snake.body[0],nx_point)

                head=snake.body[0]
                direc,max_distance=snake.direction,-1

                adjPoints=getAllAdjacents(snake) # get all adj for snake head
                for adj in adjPoints:
                    if inMap(adj):
                        temp_distance=manhattanDistance(adj,food)
                        if temp_distance>max_distance:
                            max_distance=temp_distance
                            direc=getDirection(head,adj)
                temp_nx=getAdjacent(snake.body[0],direc)
                if isValidPoint(temp_nx,snake,food): # temp_nx not in snake or out of map
                    return direc
                return None

            bestDirection=findDirection(snake,food)
            # print(bestDirection)
            if bestDirection:
                snake.move(bestDirection)
            else:
                # not exists the best direction path , game over.
                game_state = "start"
                snake = Snake()
                food = Food()
                score = 0
                continue

            # Check if the food has been eaten
            if snake.body[0] == tuple(food.position):
                snake.grow()
                food.respawn()

                while tuple(food.position) in snake.body:
                    if len(snake.body)==GRID_HEIGHT*GRID_WIDTH:  # filled
                        game_state = "start"
                        snake = Snake()
                        food = Food()
                        score = 0
                        continue
                    # print('agian food')
                    food.respawn()


                score += 1

            # Check if the snake has collided with itself or the wall
            if snake.body[0] in snake.body[1:] or \
                snake.body[0][0] < 0 or \
                snake.body[0][1] < 0 or \
                snake.body[0][0] >= GRID_HEIGHT or \
                snake.body[0][1] >= GRID_WIDTH:
                game_state = "start"
                snake = Snake()
                food = Food()
                while tuple(food.position) in snake.body:
                    food.respawn()
                score = 0
                continue

            pygame.display.update()
            clock.tick(10)

if __name__ == "__main__":
    main()

