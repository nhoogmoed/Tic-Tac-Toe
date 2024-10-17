from typing import Optional

from board import Board, Piece, Move, AllRuns, getRunIndices, applyMove, applyMoveAndPrint, isValidMove

from functools import partial

 

def getMoveFromAI(agentPiece: Piece, board: Board) -> Move:

  otherPiece = Piece.X if agentPiece == Piece.O else Piece.O

  # step three: Take first available piece, in order of middle > corner > side

  for x, y in ((0, 0), (0, 1), (0, 2), 
               (1, 0), (1, 1), (1, 2), 
               (2, 0), (2, 1), (2, 2)):


    if board[x][y] == Piece.Empty:

      return Move(agentPiece, x, y)

  raise RuntimeError(f"Ran out of moves")

 

def getMoveFromInput(agentPiece: Piece, board: Board) -> Move:

  while True:

    # Print board if available

    print("Current Board: ")

    print(board)

    # Ask agent for coords

    print(f"You are {agentPiece}, please make a move")

    x = input("Row (0 = top, 1 = middle, 2 = bottom):")

    y = input("Column (0 = left, 1 = middle, 2 = right):")

    move = Move(agentPiece, int(x), int(y))

    # validate move

    if isValidMove(move, board):

      return move

    else:

      print("---Move is invalid---\n")

 

if __name__ == "__main__":

  """

  Start a game loop with two players

  """

  board = Board()

  # The functools.partial function takes a function and some arguments, then creates

  # A new function that is the same as the first function, but with the arguments

  # Pre applied. Here we use it to pre apply the pieces used by xPicker and oPicker

  # to the given move generation functions. When you've written your AI, you can

  # replace one `getMoveFromInput` with your `getMoveFromAI` function to play

  # against your AI. Or replace both to have your AI play against itself!

  xPicker = partial(getMoveFromInput, Piece.X)

  oPicker = partial(getMoveFromAI, Piece.O)

  turn = xPicker

  # While there is not a winner, and moves can be made

  while not (win := board.getWinner()) and board.canMove():

    # execute the function "turn"

    # remember turn = [xo]Picker = a function that gets moves

    move = turn(board)

    board = applyMove(board, move)

    # switch turn to the other agent

    if turn is xPicker:

      turn = oPicker

    else:

      turn = xPicker

  print(board)

  if win:

    winner, _ = win

    print(f"{winner} wins!")

  else:  # if no moves can be made, but no winner

    print("Tie!")
