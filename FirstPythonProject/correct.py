def player_choice(board):
    position = 0
    try:
        position = int(input('Choose a position : (1-9)'))
        while True:
        #position = int(input('Choose a position : (1-9)'))
        #return position
        if position in range(1,10) or not space_check(board, position):
            return position
        else:
            print("Given space in not empty")
            continue
    except ValueError:
        print("Worng Position Entered. Please enter a number in range 1-9.")
        continue

def player_choice(board):
    position = 0
    try:
        while True:
            position = int(input('Choose a position : (1-9)'))
            if board[position] == " ":
                board[position] = 
