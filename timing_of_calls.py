#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  timing_of_calls.py
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
g = chess.Board()
import timeit

iters = 15000
setup_statement = 'import chess as chess;game = chess.Board();Nf3 = chess.Move.from_uci("c2c4")'
setup_statement2 = 'import chess as chess;game = chess.Board()'

setup_statement_improved = '''
import chess as chess
g = chess.Board()
def piece_score_difference(g):
	#start = time.time()
	#global piece_score_counter
	pieces = [chess.PAWN,chess.ROOK,chess.BISHOP,chess.KNIGHT,chess.QUEEN,chess.KING]
	piece_value =[1,10,5,5,25,1000]
	white = 0
	black =0
	for i,p in enumerate(pieces):
		white += len(g.pieces(p,chess.WHITE))*piece_value[i]
		black += len(g.pieces(p,chess.BLACK))*piece_value[i]
	#print time.time()-start
	#piece_score_counter +=1
	if g.turn:
		return white- black
	else:
		return black - white
'''


setup_statement_original = '''
import chess as chess
g = chess.Board()
def piece_score_difference(g):
	#start = time.time()
	#global piece_score_counter
	pieces = [chess.PAWN,chess.ROOK,chess.BISHOP,chess.KNIGHT,chess.QUEEN,chess.KING]
	piece_value =[1,10,5,5,25,1000]
	white = 0
	black =0
	for i,p in enumerate(pieces):
		white += len(list(g.pieces(p,chess.WHITE)))*piece_value[i]
		black += len(list(g.pieces(p,chess.BLACK)))*piece_value[i]
	#print time.time()-start
	#piece_score_counter +=1
	if g.turn:
		return white- black
	else:
		return black - white
'''




print 'Iterations examined -->',iters
'''
#setup_statement3 = 'import chess as chess;game = chess.Board();game.push("c2c4")'
a = timeit.Timer('game.is_game_over()',setup=setup_statement)
print 'check game over-->',a.timeit(iters)

b = timeit.Timer('game.copy()',setup=setup_statement)
print 'copy game-->',b.timeit(iters)


c = timeit.Timer('game.legal_moves',setup=setup_statement)
print 'legal moves-->',c.timeit(iters)

d = timeit.Timer('game.push(Nf3)',setup=setup_statement)
print 'push move (*10000) -->',d.timeit(10000)

'''
e = timeit.Timer('game.push_san("e4");game.pop()',setup=setup_statement2)
print 'push/pop move -->',e.timeit(iters)
'''
f = timeit.Timer('game.pieces(chess.PAWN,chess.WHITE)',setup=setup_statement)
print 'Pawn Serach-->',f.timeit(iters)


g = timeit.Timer('list(game.pieces(chess.PAWN,chess.WHITE))',setup=setup_statement)
print 'Pawn list-->',g.timeit(iters)

h = timeit.Timer('len(list(game.pieces(chess.PAWN,chess.WHITE)))',setup=setup_statement)
print 'Pawn count-->',h.timeit(iters)

h2 = timeit.Timer('len(game.pieces(chess.PAWN,chess.WHITE))',setup=setup_statement)
print 'Pawn count2-->',h2.timeit(iters)

h3 = timeit.Timer('str(game).count("p")',setup=setup_statement)
print 'Pawn count3-->',h3.timeit(iters)




i = timeit.Timer('game.pieces(chess.ROOK,chess.WHITE)',setup=setup_statement)
print 'ROOK Serach-->',i.timeit(iters)


j = timeit.Timer('list(game.pieces(chess.ROOK,chess.WHITE))',setup=setup_statement)
print 'ROOK list-->',j.timeit(iters)

k = timeit.Timer('len(list(game.pieces(chess.ROOK,chess.WHITE)))',setup=setup_statement)
print 'ROOK count-->',k.timeit(iters)

'''



aa = timeit.Timer('game.is_checkmate()',setup=setup_statement)
print 'checkmate?-->',aa.timeit(iters)

ab = timeit.Timer('game.result()',setup=setup_statement)
print 'result?-->',ab.timeit(iters)

l = timeit.Timer('piece_score_difference(g)',setup=setup_statement_original)
print 'Evaluate Original-->',l.timeit(iters)


n = timeit.Timer('piece_score_difference(g)',setup=setup_statement_improved)
print 'Evaluate Improved-->',n.timeit(iters)


