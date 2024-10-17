from dataclasses import dataclass, field

from enum import Enum, auto, unique

from typing import Optional

from collections.abc import Iterator, Iterable, Sequence

from functools import reduce

 

@unique

class DiagonalDirection(Enum):

  Down = 0

  Up = 1

 

@dataclass

class Diagonal():

  direction: DiagonalDirection

 

@dataclass

class Horizontal():

  row: int

 

@dataclass

class Vertical():

  col: int

 

Run = Diagonal | Horizontal | Vertical

AllRuns = ((Diagonal(DiagonalDirection.Up), Diagonal(DiagonalDirection.Down)) +

           tuple([Vertical(i) for i in range(3)]) +

           tuple([Horizontal(i) for i in range(3)]))

 

def getRunIndices(run: Run):

  match run:

    case Diagonal(DiagonalDirection.Down):

      return ((row, col) for col, row in enumerate(range(3)))

    case Diagonal(DiagonalDirection.Up):

      return ((row, 2 - col) for col, row in enumerate(range(3)))

    case Vertical(col):

      return ((row, col) for row in range(3))

    case Horizontal(row):

      return ((row, col) for col in range(3))

    case _ as unreachable:

      raise RuntimeError(f"reached unreachable case {unreachable}")

 

@unique

class Piece(Enum):

  Empty = auto()

  X = auto()

  O = auto()

 

  def __str__(self) -> str:

    if self.name == "Empty":

      return " "

    else:

      return self.name

 

  def __repr__(self) -> str:

    if self.name == "Empty":

      return "E"

    else:

      return self.name

 

def update(seq: Sequence, index: Sequence | int, value) -> Sequence:

 

  def _recurse(seq: Sequence, i: Iterator, value) -> Sequence:

    try:

      index = next(i)

      return seq[:index] + (_recurse(seq[index], i, value), ) + seq[index + 1:]

    except StopIteration:

      return value

 

  if isinstance(index, Sequence):

    return _recurse(seq, iter(index), value)

  elif isinstance(index, int):

    return _recurse(seq, iter((index, )), value)

  else:

    raise TypeError("index is not an int or Sequence")

 

@dataclass(frozen=True)

class Move:

  piece: Piece = field(hash=True)

  x: int = field(hash=True)

  y: int = field(hash=True)

 

@dataclass(frozen=True)

class Board:

  _boardArray: tuple[tuple[Piece]] = field(default=((Piece.Empty, ) * 3, ) * 3,

                                           hash=True)

 

  def getRun(self, run: Run) -> Iterable[Piece]:

    """

    Returns a generator for all the pieces along a run

    """

    return (self._boardArray[row][col] for row, col in getRunIndices(run))

 

  def getWinner(self) -> Optional[tuple[Piece, Run]]:

    """

    Returns a tuple containing the winning player and the run that won the game

    """

 

    def foldPieces(x: Optional[Piece], y: Optional[Piece]) -> Optional[Piece]:

      if x is None or y is None:

        return None

      if x == y:

        return x

      if x != y:

        return None

 

    for run in AllRuns:

      if (ret := reduce(foldPieces,

                        self.getRun(run))) not in [None, Piece.Empty]:

        return (ret, run)

    return None

 

  def canMove(self) -> bool:

    for row in self._boardArray:

      for piece in row:

        if piece is Piece.Empty:

          return True

    return False

 

  def _getBoardLines(self, row: Optional[Run]):

    """

    Can be ignored, gets the lines to draw when pretty printing a board

    """

    hori = ("┌─┬─┬─┐", "├─┼─┼─┤", "├─┼─┼─┤", "└─┴─┴─┘")

    vert = (("│", ) * 4, ) * 3

    match row:

      case None:

        return (hori, vert)

      case Horizontal(row):

        return (hori, vert[:row] + (("─", ) * 4, ) + vert[row + 1:])

      case Vertical(col):

        return ([row[:col * 2 + 1] + "┼" + row[col * 2 + 2:]

                 for row in hori], vert)

      case Diagonal(DiagonalDirection.Down):

        return ((

          "╲─┬─┬─┐",

          "├─╲─┼─┤",

          "├─┼─╲─┤",

          "└─┴─┴─╲",

        ), vert)

      case Diagonal(DiagonalDirection.Up):

        return ((

          "┌─┬─┬─╱",

          "├─┼─╱─┤",

          "├─╱─┼─┤",

          "╱─┴─┴─┘",

        ), vert)

 

  def __getitem__(self, key) -> tuple:

    return self._boardArray[key]

 

  def __iter__(self):

    return iter(self._boardArray)

 

  def __repr__(self) -> str:

    return f"Board({','.join((''.join((repr(piece) for piece in row)) for row in self._boardArray))})"

 

  def __str__(self) -> str:

    win = self.getWinner()

    winner, run = win if win else (None, None)

    horizontalLines, verticalLines = self._getBoardLines(run)

    ret = horizontalLines[0] + "\n"

    for verticalLine, horizontalLine, row in zip(verticalLines,

                                                 horizontalLines[1:],

                                                 self._boardArray):

      ret += verticalLine[0]

      for char, piece in zip(verticalLine[1:], row):

        ret += str(piece)

        ret += char

      ret += "\n" + horizontalLine + "\n"

    return ret

 

def applyMove(board: Board, move: Move) -> Board:

  if move.piece == Piece.Empty:

    raise ValueError("Cannot add an empty piece")

  if move.x > 2 | move.x < 0 | move.y > 2 | move.y < 0:

    raise IndexError("Board positions are not between 0 and 2 (inclusive)")

  if board._boardArray[move.x][move.y] != Piece.Empty:

    raise ValueError("Board position is already occupied")

  retArray = update(board._boardArray, (move.x, move.y), move.piece)

  return Board(retArray)

 

def applyMoveAndPrint(board: Board, move: Move) -> Board:

  ret = applyMove(board, move)

  print(ret)

  return ret

 

def isValidMove(move: Move, board: Board) -> bool | str:

  try:

    applyMove(board, move)

    return True

  except (ValueError, IndexError):

    return False

 

if __name__ == "__main__":

  """

  Some examples of what you can do:

  """

  board = Board()

  print(repr(board))

  print(board)

  board = applyMove(board, Move(Piece.X, 1, 1))

  board = applyMoveAndPrint(board, Move(Piece.O, 0, 1))

  print(board[1])

  print(board[1][1])

  print(f"\"{board[1][2]}\"")

  print(f"\"{repr(board[1][2])}\"")

  for row in board:

    for piece in row:

      print(repr(piece), end="")

  print()

 

