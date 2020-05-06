from IPython.display import clear_output
import random

# Create Display board
def display_board(board):
    clear_output()
    print(f'{board[7]} | {board[8]} | {board[9]}')
    print(f'{board[4]} | {board[5]} | {board[6]}')
    print(f'{board[1]} | {board[2]} | {board[3]}')

#Check Display board
test_board = ['#', 'X', 'O', 'X', 'X', 'O', 'X', 'X', 'O', 'X']
#display_board(test_board)
#display_board(test_board)

#
def player_input():
    marker = ""

    while marker!='x' and marker !='O':
        marker = input('Player-1, Choose X or O : ').upper()

        if marker == 'X':
            return('X', 'O')

        else:
            return('O', 'X')

#Verify playeer_input methos works as expected:
#player1_marker, player2_marker = player_input()

def place_marker(board, marker, position):
    board[position] = marker

#Check place_marker(board, marker, position) functionality
#place_marker(test_board, '$', 8)
#display_board(test_board)

# Check for possible wins
def win_check(board, mark):
    # check if all All row or All columns or diagonals have same marker
    #(board[1] == mark and board[2] == mark and board[3] == mark)
    # above stement can be checked for all possible combinations or use below one
    return ((board[1] == board[2] == board[3] == mark) or # for rows
    (board[4] == board[5] == board[6] == mark) or # for rows
    (board[7] == board[8] == board[9] == mark) or # for rows
    (board[1] == board[4] == board[7] == mark) or # for columns
    (board[2] == board[5] == board[8] == mark) or # for columns
    (board[3] == board[6] == board[9] == mark) or # for columns
    (board[1] == board[5] == board[9] == mark) or # for diagonals
    (board[3] == board[5] == board[7] == mark) ) # for diagonals

#display_board(test_board)
#win_check(test_board, 'X')

def choose_first():
    flip = random.randint(0,1)
    if flip == 0:
        return 'Player1'
    else:
        return 'player2'

#space_check to check if any block is still empty on board
def space_check(board, position):
    if board[position] == " " and position in range(1,10):
        return True
    else:
        print("In else block")
        return False

#check if the board is full
def full_board_check(board):
    for i in range(10):
        if space_check(board,i):
            return False
    return True

# Function to check player's next choice of block for place_marker
def player_choice(board):
    position = 0
    position = int(input('Choose a position : (1-9)'))
    #while position not in range(10) or not space_check(board, position):
        #position = int(input('Choose a position : (1-9)'))
        #return position
    if position in range(1,10) or not space_check(board, position):
        return position
    else:
        print("Worng Position Entered. Please enter a number in range 1-9.")
        position = int(input('Choose a position : (1-9)'))
        return position

#play again on User's wish
def replay():
    choice = input('Play again? Enter Yes or No : ')
    return choice == 'Yes'

#Main
print("Welcome to Tic Tac Toe!!!")

while True:
    #play the Game
    # Set up Evenrything (board, Who's First , Choose marker etc)
    the_board = [" "] * 10
    game_on = False
    player1_marker, player2_marker = player_input()

    turn = choose_first()
    print(turn + " will go first")
    play_game = input("Ready to play ? Y or N :")
    print(f'input received from user is {play_game}')
    if play_game == "Y":
        game_on = True
        print(f'input received from user is {game_on}')
    else:
        game_on = False
        print(f'input received from user is {game_on}')

    ## Game Play
    while game_on:
        # Player1 turn
        if turn == 'Player 1':
            #show the board
            display_board(the_board)
            #choose the position
            position = player_choice(the_board)
            #Place the marker on the position
            place_marker(the_board,player1_marker, position)
            # check if they won
            if win_check(the_board, player1_marker):
                display_board(the_board)
                print("Player 1 won the Game")
                game_on = False
            # check if there is a tie
            else:
                if full_board_check(the_board):
                    display_board(the_board)
                    print("Tie game")
                    game_on = False
                else:
                    turn = "Player 2"
            # No tie or no Win? Next player's turn

        # Player2 turn
        else:
            #show the board
            display_board(the_board)
            #choose the position
            position = player_choice(the_board)
            #Place the marker on the position
            place_marker(the_board, player2_marker, position)
            # check if they won
            if win_check(the_board, player2_marker):
                display_board(the_board)
                print("Player 2 won the Game")
                game_on = False
            # check if there is a tie
            else:
                if full_board_check(the_board):
                    display_board(the_board)
                    print("Tie game")
                    game_on = False
                else:
                    turn = "Player 1"

    if not replay():
        break
