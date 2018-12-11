from E4_4U import MCTS
from random import choice
import inspect
import copy
player = 'o'
enemy = 'x'
empty = '.'
width = 7
height = 6


# Connect 4 Board Object
class Board:

    # Create new board
    def __init__(self):
        self.state = {}
        for col in range(width):
            for row in range(height):
                self.state[(col,row)] = empty


    # Prints the board at the current state
    # No return
    def print_board(self,state):
        for i in range(height-1,-1,-1):
            for j in range(0,width):
                print(str(state[(j,i)]) + " ", end="")
            print()
        print()


    # Applies move to state
    # Returns new state
    def do_move(self,state,turn,move):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        new_state = copy.deepcopy(state)
        if move in new_state:
            if move in self.get_valid_moves(new_state):
                if new_state[move] == empty:
                    new_state[move] = turn
                    print("did move")
                else:
                    print("do_move: Tried to do " + str(move) + " but position is " + str(new_state[move]))
            else:
                print(self.get_valid_moves(new_state))
                print("do_move: Not a valid move")
        else:
            print("do_move: Move not in board.")
        self.new_state = new_state
        return new_state


    # Gets the best move to do given a state and a move set
    # Returns best move
    def get_best_move(self,state,moves = []):
        # TODO : Optimize move choice. Pick moves closer to middle, with more pieces around, if piece above isn't a
        #       winning move for enemy, scissors, etc.

        #if not provided any moves, get valid moves
        if not moves:
            moves = self.get_valid_moves(state)

        # check for winning/losing moves
        winning_moves = self.get_winning_moves(state,moves)
        if winning_moves:
            move = winning_moves[0][0]
        else: # if no winning/losing moves, pick random move
            move = choice(moves)
        return move


    # Get moves you can do for next turn
    # Returns valid moves at state of game
    def get_valid_moves(self,state):
        valid_moves = []
        for col in range(width):
            for row in range(height):
                
                if state[col,row] == empty:
                    print("found empty: " + str((col,row)))
                    valid_moves.append((col,row))
                    break
        return valid_moves


    # Check the valid moves and see if any are moves that will make either player win
    # Returns the winning moves for either player in a list with entries (move, player)
    # Winning moves are at beginning of list and losing moves (ie must block) are at end of list
    def get_winning_moves(self,state,valid_moves=[]):
        winning_moves = []
        players = [player,enemy]

        if not valid_moves: # this will let us check if any moves are winning/losing moves
            valid_moves = self.get_valid_moves(state)

        for turn in players: # check for both player and enemy
            for move in valid_moves:
                winnable = 0
                # check vertical win
                if move[1] > 2:
                    for i in range(1,4):
                        if (state[(move[0],move[1]-i)] == turn):
                            if winnable == 2:
                                if turn == player:
                                    winning_moves.insert(0,(move,turn))
                                else:
                                    winning_moves.append((move,turn))
                            else:
                                winnable += 1
                        else:
                            break

                winnable = 0
                #horizontal win
                for k in range(-1,2,2): # check to both left and right
                    if move not in winning_moves: # haven't already found win from one direction
                        for i in range(1,4):
                            if (move[0]-i*k,move[1]) in state: # check 3 left/right
                                if (state[(move[0]-i*k,move[1])] == turn):
                                    if winnable == 2:
                                        if turn == player:
                                            winning_moves.insert(0,(move,turn))
                                        else:
                                            winning_moves.append((move,turn))
                                        break
                                    else:
                                        winnable += 1
                                else:
                                    break

                winnable = 0
                # / win
                for k in range(-1,2,2): # check bottom left and top right directions
                    if move not in winning_moves: # haven't already found win from one direction
                        for i in range(1,4):
                            if (move[0]-i*k,move[1]-i*k) in state:
                                if (state[(move[0]-i*k,move[1]-i*k)] == turn):
                                    if winnable == 2:
                                        if turn == player:
                                            winning_moves.insert(0,(move,turn))
                                        else:
                                            winning_moves.append((move,turn))
                                        break
                                    else:
                                        winnable += 1
                                else:
                                    break

                winnable = 0
                # \ win
                for k in range(-1,2,2): # check bottom right and top left directions
                    if move not in winning_moves: # haven't already found win from one direction
                        for i in range(1,4):
                            if (move[0]-i*k,move[1]+i*k) in state:
                                if (state[(move[0]-i*k,move[1]+i*k)] == turn):
                                    if winnable == 2:
                                        if turn == player:
                                            winning_moves.insert(0,(move,turn))
                                        else:
                                            winning_moves.append((move,turn))
                                        break
                                    else:
                                        winnable += 1
                                else:
                                    break

        return winning_moves


    # Checks if game at state is over by looking at the last possible moves (top piece of every row)
    # Returns (game ended, player that won)
    def is_ended(self,state):
        last_moves = []
        for col in range(width):
            for row in range(height):
                if state[col,row] == empty: # if we reach an empty spot (going up vertically)
                    if (col,row-1) in state: # then add the spot right before empty spot
                        last_moves.append((col,row-1))
                    break
                elif row == height - 1: # if we reach the top
                    last_moves.append((col,row))
                    
            
        won = self.get_winning_moves(state,last_moves)
        # won will contains wins for either player
        # so we must check if that player actually owns the piece.
        for move in won: 
            if state[move[0]] != move[1]:
                won.remove(move)
                
        if len(won) == 0:
            return (False,None)
        else:
            return (True,won)


b = Board()
state = b.state
j=0
while not b.is_ended(b.state)[0]:
    print("cat")
    nextmove=MCTS(b)
    if j%2 == 0:
        b.do_move(state,player,nextmove)
    else:
        b.do_move(state,enemy,nextmove)
    b.print_board(state)
    print("fish")
    
b.print_board(b.state)

print(b.get_valid_moves(b.state))
print(b.get_winning_moves(b.state))
print(b.is_ended(b.state))
