
import random
import chess
import chess.svg
from flask import Flask
import tensorflow as tf
import math
import numpy
app = Flask(__name__)

Board = chess.Board()

def rollout(board,rolls,side):
    result = 0
    fen = board.board_fen()
    for roll in range(rolls):
        board.set_board_fen(fen)
        while (board.is_game_over() == False):
            List = list(board.legal_moves)
            move = random.choice(List)
            board.push(move)


        res = board.result()

        res = res.split("-")[side]

        if res == "1/2":
            res = "0.5"
        res = float(res)

        result += res
    c= 2
    si = result+c*math.sqrt(numpy.log(rolls))
    return si


def makeMove(board,side):
    cboard = board
    roll = 0
    finalMove = ""
    List =list(board.legal_moves)
    for aMove in List:
        aMove = str(aMove)
        aMove = chess.Move.from_uci(aMove)

        board = cboard.copy()
        #print(board)
        board.push(aMove)
        new_rollout = rollout(board,20000,side)
        if (new_rollout>roll):
            roll = new_rollout
            finalMove= aMove
    return finalMove


@app.route("/")
def playGame():

    while (Board.is_game_over() == False):
        Board.push(makeMove(Board, 0))
        print(Board)
        Board.push(makeMove(Board, 1))
        print(Board)
        Brd = chess.BaseBoard(Board.board_fen())
    return (chess.svg.board(Brd))
playGame()