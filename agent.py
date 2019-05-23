#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Written by Jincheng Tao & Donghan Shi, 16/04/2019

import numpy as np
import math
import sys
import socket

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    global AIplayer
    
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        return AIplayer.second_move(int(args[0])-1,int(args[1])-1)
    elif command == "third_move":
        return AIplayer.third_move(int(args[0])-1, int(args[1])-1, int(args[2])-1)
    elif command == "next_move": 
        return AIplayer.next_move(int(args[0])-1)
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# TTT_AI class represents the Nine_Board_Tic_Tac_Toe AI
class TTT_AI(object):

    # default depth is 5, we can set parameter to modify searching depth
    def __init__(self, depth=5):
        self.move = None                            # current move
        self.depth = depth                          # current depth
        self.board = np.zeros((9,9), dtype=np.int8) # Tic_Tac_Toe board full of 0s
        self.step = 0                               # current step
        self.balance = 0
        self.offensive = 1
        
        # 7 lines' coordinates
        self.lines = [[0, 1, 2],
                      [3, 4, 5],
                      [6, 7, 8],
                      [0, 3, 6],
                      [1, 4, 7],
                      [2, 5, 8],
                      [0, 4, 8],
                      [2, 4, 6]]
        
        # all positions' values
        self.pos_value = np.array([[90, 95, 100, 95, 105, 96, 100, 96, 100],
                                   [103, 89, 103, 100, 108, 100, 104, 98, 104],
                                   [100, 95, 90, 96, 105, 95, 100, 96, 100],
                                   [103, 100, 104, 89, 108, 98, 103, 100, 104],
                                   [97, 92, 97, 92, 92, 92, 97, 92, 97],
                                   [104, 100, 103, 98, 108, 89, 104, 100, 103],
                                   [100, 96, 100, 95, 105, 96, 90, 95, 100],
                                   [104, 98, 104, 100, 108, 100, 103, 89, 103],
                                   [100, 96, 100, 96, 105, 95, 100, 95, 90]], dtype=np.int8)

    # defensive situation
    def second_move(self, pos1, pos2):
        self.board[pos1, pos2] = -1
        self.step += 1
        self.offensive = 1
        self.balance = self.depth%2
        self.alphabeta(self.board, pos2)
        self.board[pos2, self.move] = 1
        self.step += 1
        return self.move+1

    # offensive situation   
    def third_move(self, pos1, pos2, pos3):
        self.board[pos1, pos2] = 1
        self.board[pos2, pos3] = -1
        self.step += 2
        self.offensive = -1
        self.balance = (self.depth+1)%2
        self.alphabeta(self.board, pos3)
        self.board[pos3, self.move] = 1
        self.step += 1
        return self.move+1

    # generalisation    
    def next_move(self, pos):
        self.board[self.move, pos] = -1
        self.step += 1
        self.alphabeta(self.board, pos)
        self.board[pos, self.move] = 1
        self.step += 1
        return self.move+1

    # starts alpha-beta pruning searching and returns the best move
    def alphabeta(self, board, opp):
        subboard = board[opp]
        
        # judge whether exists the situation that can checkmate directly
        for line in self.lines:
            if sum(subboard[line]) == 2:
                self.move = line[np.where(subboard[line] == 0)[0][0]]
                return

        # set the value of alpha and beta
        alpha, beta = -math.inf, math.inf
        # In the begining of 10 moves, we reduce searching depth
        if self.step<=10:
            depth = self.depth-2
        else:
            depth = self.depth
        v = -math.inf
        for i in np.where(board[opp] == 0)[0]:
            board[opp, i] = 1
            v = max(v, self.min_decision(board, opp, i, depth-1, alpha, beta))
            board[opp, i] = 0
            if alpha < v:           # if v > alpha, update move
                self.move = i
            alpha = max(alpha, v)   # if v > alpha, update alpha
            if beta <= alpha:       # if beta <= alpha, break and prune the tree
                break

    def max_decision(self, board, last_move, move, depth, alpha, beta):

        # Before making max_decision, we only care about whether or not can directly win
        if self.win(board[move]):
            return 3000

        # find all available moves in subboard
        next_moves = np.where(board[move] == 0)[0]
        if not next_moves.size:
            return 0
        
        # return heuristic value when reach limited depth
        elif depth == 0:
            return self.value(board)
        
        v = -math.inf
        for i in next_moves:
            board[move, i] = 1
            v = max(v, self.min_decision(board, move, i, depth-1, alpha, beta))
            board[move, i] = 0
            alpha = max(alpha, v)   # if v > alpha, update alpha
            if beta <= alpha:       # if beta <= alpha, break and prune the tree
                break
        return v
    
    def min_decision(self, board, last_move, move, depth, alpha, beta):

        # We assume the oppopent can always make the optimal choice
        # Before making min_decision, we only care about whether or not can directly lose
        if self.lose(board[move]):
            return -3000

        # find all available moves in subboard
        next_moves = np.where(board[move] == 0)[0]
        if not next_moves.size:
            return 0
        
        # return heuristic value when reach limited depth
        elif depth == 0:
            return self.value(board)
        
        v = math.inf
        for i in next_moves:
            board[move, i] = -1
            v = min(v, self.max_decision(board, move, i, depth-1, alpha, beta))
            board[move, i] = 0
            beta = min(beta, v)     # if v < beta, update beta
            if beta <= alpha:       # if beta <= alpha, break and prune the tree
                break
        return v

    # check if exists a line containing only two ls
    def win(self, board):
        for line in self.lines:
            if sum(board[line]) == 2:
                return True
        return False

    # check if exists a line containing only two -ls
    def lose(self, board):
        for line in self.lines:
            if sum(board[line]) == -2:
                return True
        return False

    # calculate heuristic value
    def value(self, board):
        value = 0
        num = [0]*9

        # the number of the empty positions which can point to subboard_i
        for i in range(9):
            num[i] = sum(board[:, i] == 0)

        # calculate heuristic value  
        for i, subboard in enumerate(board):
            for line in self.lines:
                equl = 0
                points = subboard[line]
                sum_value = sum(points)
                if sum_value == 2:
                    equl += 6
                elif sum_value == -2:
                    equl -= 6
                elif sum(points == 0) == 2:
                    if sum_value == 1:
                        equl += 1
                    elif sum_value == -1:
                        equl -= 1
                value += equl*num[i]

        # In the begining of 10 moves, we consider positions' values
        if self.step <= 10:
            value += (np.sum(board*self.pos_value)-self.offensive*self.balance*99)*9
        return value

def main():
    global AIplayer
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)
    s.connect(('localhost', port))

    # Usage: ./agent.py -p (port) (depth)
    if len(sys.argv)>=4:
        AIplayer.depth = int(sys.argv[3])
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())
    
if __name__ == "__main__":
    AIplayer = TTT_AI()
    main()
