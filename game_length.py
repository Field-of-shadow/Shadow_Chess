#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Draft1.py
#  
#  Copyright 2016 dragon <dragon@BLACKDRAGON>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import random 
import time

import numpy as np

import chess as chess

'''

def random_game():
	start = time.time()
	game = chess.Board()
	while not game.is_game_over():
		wander = game.copy()
		#print wander
		if not game.turn:
			_,new_board = best_move(wander,3,piece_score_difference)
			#_,new_board = best_move(wander,1)
		else:
			_,new_board = best_move(wander,1,random_move)  #random choice
		#print new_board
		game = new_board.copy()
		if game.is_seventyfive_moves() or game.is_fivefold_repetition() or game.fullmove_number >= 75:
			break
	#print piece_score_counter		
	return game.fullmove_number,game.result(),time.time()-start

def piece_score_difference(g):
	#start = time.time()
	global piece_score_counter
	pieces = [chess.PAWN,chess.ROOK,chess.BISHOP,chess.KNIGHT,chess.QUEEN,chess.KING]
	piece_value =[1,10,5,5,25,100]
	white = 0
	black =0
	for i,p in enumerate(pieces):
		white += len(list(g.pieces(p,chess.WHITE)))*piece_value[i]
		black += len(list(g.pieces(p,chess.BLACK)))*piece_value[i]
	#print time.time()-start
	piece_score_counter +=1
	if g.turn:
		return white- black
	else:
		return black - white
	
	
def random_move(g):
	return random.random()
	
def best_move(game,depth,evaluate):
	if depth ==0 or game.is_game_over():
		return evaluate(game),game
	#print game
	if game.turn:  # whites turn
		bestscore = -1*np.inf
		bestmove = None
		for m in game.legal_moves:
			test_move = game.copy()
			test_move.push(m)
			#print test_move
			score,move = best_move(test_move,depth-1,evaluate)
			#print score,move
			if score >bestscore:
				bestscore = score
				bestmove = test_move
			elif score == bestscore:
				bestmove = random.choice((move,bestmove))
		return bestscore,bestmove
	else: #black's turn
		bestscore = np.inf
		bestmove = None
		for m in game.legal_moves:
			test_move = game.copy()
			test_move.push(m)
			score,move = best_move(test_move,depth-1,evaluate)
			if score <bestscore:
				bestscore = score
				bestmove = test_move
			elif score == bestscore:
				bestmove = random.choice((move,bestmove))
		return bestscore,bestmove


white_wins =0
black_wins = 0
draws =0
running_time=0
total_piece_score_counter = 0
total_games =10
total_moves = 0
for i in range(total_games):
	piece_score_counter=0
	m,r,t= random_game()			
	total_moves+=m
	if r == '1-0':
		white_wins+=1
	elif r== '0-1':
		black_wins+=1
	else:
		draws+=1
	running_time+=t
	#if i %2 ==0:
	print i+1,': white->',white_wins,'black->',black_wins,'draws->',draws,'time->',t,'moves->',m,'counts->',piece_score_counter
	total_piece_score_counter+=piece_score_counter
print '#'*75
print total_games,': white->',white_wins,'black->',black_wins,'draws->',draws,'time->',running_time,'total moves->',total_moves,'counts->',total_piece_score_counter
	
'''

evaluate = 0
MOVES = []
EVALUATES = []
print evaluate
def make_move(g,d,p):
	global evaluate
	if d==0:
		evaluate +=1
		return
	moves = [m for m in game.legal_moves]
	#print moves
	random.shuffle(moves)
	moves = moves[:len(moves)*p/100]
	for m in moves:
		make_move(game.push(m),d-1,p-5)
		game.pop()
	MOVES.append(len(moves))

percent = 50
init_depth =5
move_counter = 1
game = chess.Board()
while not game.is_game_over() and not game.is_seventyfive_moves():
	start = time.time()
	if game.halfmove_clock <35:
		make_move(game,init_depth,percent)
	else:
		make_move(game,init_depth+3,percent-15)
		
	moves = [m for m in game.legal_moves]
	random.shuffle(moves)
	game.push(moves[0])
	print move_counter, evaluate,time.time()-start
	EVALUATES.append(evaluate)
	evaluate = 0
	move_counter +=1
	if game.halfmove_clock >50:
		break
	#print game
print 'avg moves considered',np.average(MOVES)
print 'avg evaluations',np.average(EVALUATES)
