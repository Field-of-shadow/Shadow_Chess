#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  parse_PGNs.py
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


import chess as chess
import chess.pgn as pgn

import random as random
import time as time

import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier

import matplotlib.pyplot as plt

start = time.time()

with open ('PGN_files\games.pgn') as games:
	offsets = pgn.scan_headers(games)
	num_games = len([1 for i in offsets])
	print '# of games -->',num_games


# for diagnostics
#num_games /= 75
early_boards = []
late_boards = []
results  = []


##
## won or loss games with ply > 10
##

with open ('PGN_files\games.pgn') as games:
	for _ in range(num_games):
		g = pgn.read_game(games)
		
		if not g.headers['Result'] == '1-0' and not g.headers['Result'] == '0-1':
			continue
		
		plys = int(g.headers['PlyCount'])
		if not plys >10:
			continue
		
		if g.headers['Result'] == '1-0':
			results.append(1)
		else:
			results.append(-1)
		
		
			
		node = g
		for _ in range(random.randint(1,plys/2)):
			next_node = node.variation(0)
			node.board().san(next_node.move)
			node = next_node
		early_boards.append(node)
		
		node = g
		for _ in range(random.randint(plys/2,plys-1)):
			next_node = node.variation(0)
			node.board().san(next_node.move)
			node = next_node
		late_boards.append(node)

print '# of games with a winner -->',len(results)
#print results		
print 'partial time -->',time.time()-start

##
## Get drawn games as ~ one third the total number of games
##
'''
with open ('PGN_files\games.pgn') as games:
	for c in range(num_games):
		g = pgn.read_game(games)
		
		if g.headers['Result'] == '1-0' or g.headers['Result'] == '0-1':
			continue
		
		
		results.append(0)
		
		plys = int(g.headers['PlyCount'])
		if not plys >10:
			continue
			
		node = g
		for _ in range(random.randint(1,plys/2)):
			next_node = node.variation(0)
			node.board().san(next_node.move)
			node = next_node
		early_boards.append(node)
		
		node = g
		for _ in range(random.randint(plys/2,plys-1)):
			next_node = node.variation(0)
			node.board().san(next_node.move)
			node = next_node
		late_boards.append(node)
		
		if c >= len(results)/2:
			break
'''
print '# of total games -->',len(results)

print 'total time -->',time.time()-start
		

#print late_boards[10].board()		
		

PIECES = [chess.PAWN,chess.ROOK,chess.KNIGHT,chess.BISHOP,chess.QUEEN,chess.KING]

def list_to_array(L):
	a = np.zeros(64)
	for l in L:
		a[l] = 1.
	return a
	
def encode_boards_v1(board):
	#encoded_boards = []		
	#for b in boards:
	encoded_board = []
	for piece in (PIECES):
		encoded_board = np.concatenate((encoded_board,list_to_array(board.board().pieces(piece,chess.WHITE)),
			list_to_array(board.board().pieces(piece,chess.BLACK))))
			#print encoded_board
		#print b.board()
		#print encoded_board
		#encoded_boards.append(encoded_board)
	return encoded_board
		

encoded_board = []
for lb in late_boards:
	encoded_board.append(encode_boards_v1(lb))

#data = zip(encoded_board,results)

model = LogisticRegression()

#= RandomForestRegressor(n_estimators = 250)

cut = int(len(results)-len(results)*.2)
print cut

print len(encoded_board),len(results)
model.fit(encoded_board[:cut],results[:cut])

predicts = model.predict(encoded_board[cut:])
real = results[cut:]

print len(predicts),len(real)
print metrics.accuracy_score(real,predicts)
'''
for i,proba in enumerate(model.predict_proba(encoded_board[cut:])):
	if proba[0] < .2 or proba[0] >0.8:
		print proba,predicts[i],real[i]
'''

### dummy comparisons
dummy_uniform = DummyClassifier(strategy = 'uniform')
dummy_uniform.fit(encoded_board[:cut],results[:cut])

dummy_uniform_predicts = dummy_uniform.predict(encoded_board[cut:])
print metrics.accuracy_score(real,dummy_uniform_predicts)


dummy_stratified = DummyClassifier(strategy = 'stratified')
dummy_stratified.fit(encoded_board[:cut],results[:cut])

dummy_stratified_predicts = dummy_stratified.predict(encoded_board[cut:])
print metrics.accuracy_score(real,dummy_stratified_predicts)


#print zip(model.predict(encoded_board[cut:]),results[cut:])



#plt.scatter(rf.predict(encoded_board[cut:]),results[cut:])
#plt.show()
'''
correct =0
close = 0
incorrect = 0
for p,r in zip(rf.predict(encoded_board[cut:]),results[cut:]):
	if p == r:
		correct +=1
	elif (p==1 and r == -1) or (p==-1 and r==1):
		incorrect +=1
	else:
		close +=1

print 'Training examples -->',cut
print 'Exact -->', correct
print 'Close -->', close
print 'Incorrect -->', incorrect
'''

